# How to Create a Pinokio Script

This guide explains how to create a Pinokio script based on the Higgs Audio V2 Enhanced implementation. Pinokio is a package manager for AI applications that uses JavaScript configuration files to define installation, startup, and management workflows.

## Higgs Audio V2 Enhanced - Real Implementation

The Higgs Audio V2 Enhanced Pinokio package demonstrates advanced text-to-speech capabilities with:

- **Multi-platform PyTorch support** (Windows NVIDIA/AMD, Linux NVIDIA/ROCm, macOS)
- **UV package manager** for lightning-fast installations
- **Gradio web interface** with proper event monitoring
- **HuggingFace model downloads** without authentication requirements
- **Proper installation order** to prevent PyTorch version conflicts
- **Cross-platform file operations** for Windows and Unix-like systems
- **Real-time status updates** and dynamic menu generation

## Core Files Structure

A typical Pinokio script consists of these JavaScript files:

```
your-project/
├── pinokio.js      # Main configuration and menu system
├── install.js      # Installation workflow
├── start.js        # Application startup
├── update.js       # Update workflow
├── reset.js        # Reset/cleanup workflow
├── link.js         # Deduplication workflow (optional)
├── torch.js        # PyTorch installation (optional)
└── icon.png        # Project icon
```

## 1. Main Configuration (`pinokio.js`)

The main configuration file defines your project metadata and dynamic menu system:

```javascript
const path = require('path')

module.exports = {
  version: "3.7",
  title: "<TITLE>",
  description: "",
  icon: "<ICON>",
  menu: async (kernel, info) => {
    let installed = info.exists("app/env")
    let running = {
      install: info.running("install.js"),
      start: info.running("start.js"),
      update: info.running("update.js"),
      reset: info.running("reset.js"),
      link: info.running("link.js")
    }
    
    // Show different menus based on state
    if (running.install) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Installing",
        href: "install.js",
      }]
    } else if (installed) {
      if (running.start) {
        let local = info.local("start.js")
        if (local && local.url) {
          return [{
            default: true,
            icon: "fa-solid fa-rocket",
            text: "Open Web UI",
            href: local.url,
          }, {
            icon: 'fa-solid fa-terminal',
            text: "Terminal",
            href: "start.js",
          }]
        } else {
          return [{
            default: true,
            icon: 'fa-solid fa-terminal',
            text: "Terminal",
            href: "start.js",
          }]
        }
      } else if (running.update) {
        return [{
          default: true,
          icon: 'fa-solid fa-terminal',
          text: "Updating",
          href: "update.js",
        }]
      } else if (running.reset) {
        return [{
          default: true,
          icon: 'fa-solid fa-terminal',
          text: "Resetting",
          href: "reset.js",
        }]
      } else if (running.link) {
        return [{
          default: true,
          icon: 'fa-solid fa-terminal',
          text: "Deduplicating",
          href: "link.js",
        }]
      } else {
        // Main menu when installed but not running
        return [{
          default: true,
          icon: "fa-solid fa-power-off",
          text: "Start",
          href: "start.js",
        }, {
          icon: "fa-solid fa-plug",
          text: "Update",
          href: "update.js",
        }, {
          icon: "fa-solid fa-plug",
          text: "Install",
          href: "install.js",
        }, {
          icon: "fa-solid fa-file-zipper",
          text: "<div><strong>Save Disk Space</strong><div>Deduplicates redundant library files</div></div>",
          href: "link.js",
        }, {
          icon: "fa-regular fa-circle-xmark",
          text: "<div><strong>Reset</strong><div>Revert to pre-install state</div></div>",
          href: "reset.js",
          confirm: "Are you sure you wish to reset the app?"
        }]
      }
    } else {
      // Not installed - show install option
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Install",
        href: "install.js",
      }]
    }
  }
}
```

### Advanced Menu Features

You can create nested menus and platform-specific options:

```javascript
// Platform-specific menus
if (kernel.platform === "darwin") {
  // macOS specific options
} else {
  // Windows/Linux options
}

// Nested menus
return [{
  icon: "fa-solid fa-power-off",
  text: "Start Options",
  menu: [{
    icon: "fa-solid fa-cube",
    text: "Basic Mode",
    href: "start.js",
    params: { mode: "basic" }
  }, {
    icon: "fa-solid fa-bolt-lightning",
    text: "Advanced Mode",
    href: "start.js",
    params: { mode: "advanced" }
  }]
}]
```

## 2. Installation Script (`install.js`)

Defines the installation workflow using the proven installation order:

```javascript
module.exports = {
  run: [
    // Clone the Higgs Audio V2 Enhanced repository
    {
      method: "shell.run",
      params: {
        message: "git clone https://github.com/PierrunoYT/HiggsAudio-V2-Local.git app"
      }
    },
    
    // Clone and install Higgs Audio package
    {
      method: "shell.run",
      params: {
        path: "app",
        message: "git clone https://github.com/boson-ai/higgs-audio.git temp_higgs"
      }
    },
    
    // Install main app dependencies first (using UV for speed)
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install -r requirements.txt"
      }
    },

    // Install boson_multimodal package in development mode - use main environment
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "pip install -e temp_higgs/"
      }
    },

    // Install PyTorch with appropriate CUDA support (AFTER all other packages to prevent version conflicts)
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          venv: "env",
          path: "app"
        }
      }
    },
    
    // Install HuggingFace Hub for authentication (using UV for speed)
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install huggingface-hub"
      }
    },
    
    // Download Higgs Audio V2 models from Hugging Face (public models, no auth required)
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "hf download PierrunoYT/higgs-audio-v2-generation-3B-base --local-dir models/higgs-audio-v2-generation-3B-base --repo-type model"
      }
    },
    
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "hf download PierrunoYT/higgs-audio-v2-tokenizer --local-dir models/higgs-audio-v2-tokenizer --repo-type model"
      }
    },
    
    // Final verification of all components
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "python -c \"from boson_multimodal.serve.serve_engine import HiggsAudioServeEngine; print('All imports working correctly')\""
      }
    },
    
    // Create a setup completion marker
    {
      method: "fs.write",
      params: {
        path: "app/INSTALLATION_COMPLETE.txt",
        text: "Higgs Audio V2 Enhanced installation completed successfully.\n\nNext steps:\n1. Start the application using the Start button\n2. Open the web interface at the provided URL\n3. Begin generating audio with text-to-speech and voice cloning features\n\nFor support, check the README.md file.\n\nNote: All models are public and no HuggingFace authentication required."
      }
    }
  ]
}
```

### Installation Methods

- `shell.run`: Execute shell commands
- `script.start`: Run another script
- `fs.rm`: Remove files/directories
- `fs.link`: Create symbolic links

### Conditional Installation

Use `when` conditions for platform or GPU-specific installations:

```javascript
{
  when: "{{platform === 'linux' && gpu === 'nvidia'}}",
  method: "shell.run",
  params: {
    message: "pip install torch --index-url https://download.pytorch.org/whl/cu118"
  }
}
```

## 3. Startup Script (`start.js`)

Defines how to start your application:

```javascript
module.exports = async (kernel) => {
  const port = await kernel.port()  // Get available port
  
  return {
    daemon: true,  // Keep running in background
    run: [
      // Start the Gradio interface
      {
        method: "shell.run",
        params: {
          venv: "env",
          path: "app",
          env: {
            GRADIO_SERVER_PORT: port.toString(),
            GRADIO_SERVER_NAME: "0.0.0.0"
          },
          message: `python gradio_interface.py --port ${port} --host 0.0.0.0`,
          on: [{
            // Wait for Gradio server to start - look for the running message
            event: "/Running on local URL:.*http:\/\/[0-9.:]+:[0-9]+/",
            done: true
          }, {
            // Alternative pattern for Gradio startup
            event: "/Running on public URL:.*https:\/\/[a-zA-Z0-9.-]+\.gradio\.live/",
            done: true
          }, {
            // Fallback pattern for server startup
            event: "/Gradio app running/",
            done: true
          }, {
            // Generic localhost pattern
            event: `/http:\/\/localhost:${port}/`,
            done: true
          }]
        }
      },
      
      // Set the local URL for the "Open Web UI" button
      {
        method: "local.set",
        params: {
          url: `http://localhost:${port}`
        }
      },
      
      // Log success message
      {
        method: "log",
        params: {
          text: `🎤 Higgs Audio V2 Enhanced is running at http://localhost:${port}`
        }
      }
    ]
  }
}
```

### Event Monitoring

Monitor shell output for specific patterns. The Higgs Audio V2 implementation shows comprehensive Gradio monitoring:

```javascript
on: [{
  // Wait for Gradio server to start - look for the running message
  event: "/Running on local URL:.*http:\\/\\/[0-9.:]+:[0-9]+/",
  done: true
}, {
  // Alternative pattern for Gradio startup
  event: "/Running on public URL:.*https:\\/\\/[a-zA-Z0-9.-]+\\.gradio\\.live/",
  done: true
}, {
  // Fallback pattern for server startup
  event: "/Gradio app running/",
  done: true
}, {
  // Generic localhost pattern
  event: `/http:\\/\\/localhost:${port}/`,
  done: true
}]
```

**Why Multiple Patterns?** Gradio can output different startup messages depending on configuration, network settings, and versions. Having multiple patterns ensures reliable detection across different environments.

## 4. PyTorch Installation (`torch.js`)

Handle PyTorch installation across platforms with latest optimizations:

```javascript
module.exports = {
  run: [
    // Windows NVIDIA with advanced optimizations
    {
      when: "{{platform === 'win32' && gpu === 'nvidia'}}",
      method: "shell.run",
      params: {
        venv: "{{args && args.venv ? args.venv : null}}",
        path: "{{args && args.path ? args.path : '.'}}",
        message: [
          "uv pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 {{args && args.xformers ? 'xformers' : ''}} --index-url https://download.pytorch.org/whl/cu128 --force-reinstall --no-deps",
          "{{args && args.triton ? 'uv pip install -U triton-windows' : ''}}",
          "{{args && args.sageattention ? 'uv pip install https://github.com/woct0rdho/SageAttention/releases/download/v2.1.1-windows/sageattention-2.1.1+cu128torch2.7.0-cp310-cp310-win_amd64.whl' : ''}}"
        ]
      },
      next: null
    },
    
    // Windows AMD GPU support
    {
      when: "{{platform === 'win32' && gpu === 'amd'}}",
      method: "shell.run",
      params: {
        venv: "{{args && args.venv ? args.venv : null}}",
        path: "{{args && args.path ? args.path : '.'}}",
        message: "uv pip install torch-directml torchaudio torchvision numpy==1.26.4"
      },
      next: null
    },
    
    // Windows CPU fallback
    {
      when: "{{platform === 'win32' && (gpu !== 'nvidia' && gpu !== 'amd')}}",
      method: "shell.run",
      params: {
        venv: "{{args && args.venv ? args.venv : null}}",
        path: "{{args && args.path ? args.path : '.'}}",
        message: "uv pip install torch torchvision torchaudio numpy==1.26.4"
      },
      next: null
    },
    
    // macOS (Apple Silicon and Intel)
    {
      when: "{{platform === 'darwin'}}",
      method: "shell.run",
      params: {
        venv: "{{args && args.venv ? args.venv : null}}",
        path: "{{args && args.path ? args.path : '.'}}",
        message: "uv pip install torch torchvision torchaudio"
      },
      next: null
    },
    
    // Linux NVIDIA with optimizations
    {
      when: "{{platform === 'linux' && gpu === 'nvidia'}}",
      method: "shell.run",
      params: {
        venv: "{{args && args.venv ? args.venv : null}}",
        path: "{{args && args.path ? args.path : '.'}}",
        message: [
          "uv pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 {{args && args.xformers ? 'xformers' : ''}} --index-url https://download.pytorch.org/whl/cu128 --force-reinstall --no-deps",
          "{{args && args.sageattention ? 'uv pip install git+https://github.com/thu-ml/SageAttention.git' : ''}}"
        ]
      },
      next: null
    },
    
    // Linux AMD (ROCm support)
    {
      when: "{{platform === 'linux' && gpu === 'amd'}}",
      method: "shell.run",
      params: {
        venv: "{{args && args.venv ? args.venv : null}}",
        path: "{{args && args.path ? args.path : '.'}}",
        message: "uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2.4 --force-reinstall --no-deps"
      },
      next: null
    },
    
    // Linux CPU fallback
    {
      when: "{{platform === 'linux' && (gpu !== 'amd' && gpu !=='nvidia')}}",
      method: "shell.run",
      params: {
        venv: "{{args && args.venv ? args.venv : null}}",
        path: "{{args && args.path ? args.path : '.'}}",
        message: "uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
      },
      next: null
    }
  ]
}
```

### Advanced PyTorch Features

The updated torch.js includes support for:

- **PyTorch 2.7.0**: Latest version with performance improvements
- **CUDA 12.8**: Latest CUDA support for NVIDIA GPUs
- **UV Package Manager**: Lightning-fast installation speeds
- **Force Reinstall**: `--force-reinstall --no-deps` ensures clean PyTorch installation without dependency conflicts
- **XFormers**: Memory-efficient attention mechanisms (optional)
- **Triton**: GPU kernel optimization for Windows (optional)
- **SageAttention**: Advanced attention optimization (optional)
- **AMD GPU Support**: DirectML for Windows, ROCm for Linux
- **Proper Fallbacks**: CPU-only installation when GPU unavailable

### Optional Parameters

You can pass additional parameters to enable optimizations:

```javascript
{
  method: "script.start",
  params: {
    uri: "torch.js",
    params: {
      venv: "env",
      path: "app",
      xformers: true,      // Enable XFormers
      triton: true,        // Enable Triton (Windows)
      sageattention: true  // Enable SageAttention
    }
  }
}
```

## 5. Update Script (`update.js`)

Handle project updates with a simple git pull approach:

```javascript
module.exports = {
  run: [{
    method: "shell.run",
    params: {
      message: "git pull"
    }
  }, {
    method: "shell.run",
    params: {
      path: "app",
      message: "git pull"
    }
  }]
}
```

## 6. Reset Script (`reset.js`)

Clean reset functionality using Pinokio's filesystem removal:

```javascript
module.exports = {
  run: [{
    method: "fs.rm",
    params: {
      path: "app"
    }
  }]
}
```

## 7. Deduplication Script (`link.js`) - Optional

Save disk space by deduplicating redundant library files. This is particularly useful for projects with large dependencies:

```javascript
module.exports = {
  run: [{
    method: "fs.link",
    params: {
      venv: "app/env"
    }
  }]
}
```

### Key Features of the Deduplication Script:

- **Disk Space Savings**: Removes duplicate files and creates symbolic links
- **Preserves Functionality**: Applications continue to work normally
- **Safe Operation**: Only affects redundant library files
- **User-Friendly**: Clear menu description with HTML formatting

### Menu Integration:

The deduplication feature is integrated into the main menu with rich HTML formatting:

```javascript
{
  icon: "fa-solid fa-file-zipper",
  text: "<div><strong>Save Disk Space</strong><div>Deduplicates redundant library files</div></div>",
  href: "link.js",
}
```

This provides users with a clear understanding of what the operation does before they run it.

## 8. Customizing the Template

The current `pinokio.js` uses placeholder values that should be customized for your specific project:

### Required Customizations:

```javascript
module.exports = {
  version: "3.7",                    // Keep current or update
  title: "<TITLE>",                  // Replace with your project name
  description: "",                   // Add your project description
  icon: "<ICON>",                    // Replace with your icon filename
  // ... rest of configuration
}
```

### Example Customization:

```javascript
module.exports = {
  version: "1.0.0",
  title: "My AI Project",
  description: "Advanced AI application with web interface and GPU acceleration",
  icon: "my-project-icon.png",
  menu: async (kernel, info) => {
    // ... same menu logic
  }
}
```

### Customization Checklist:

1. **Title**: Replace `<TITLE>` with your project name
2. **Description**: Add a meaningful project description
3. **Icon**: Replace `<ICON>` with your icon filename (place in project root)
4. **Menu Text**: Customize menu text to match your application
5. **Version**: Set appropriate version number

## Template Variables

Pinokio supports template variables in double braces:

- `{{platform}}` - Operating system (win32, darwin, linux)
- `{{gpu}}` - GPU type (nvidia, amd, cpu)
- `{{args.paramName}}` - Parameters passed from menu
- `{{which('command')}}` - Find command path

## Environment Variables

Set environment variables for shell commands:

```javascript
{
  method: "shell.run",
  params: {
    env: {
      CUDA_VISIBLE_DEVICES: "0",
      PYTHONPATH: "/custom/path"
    },
    message: "python script.py"
  }
}
```

## Best Practices

1. **Use UV Package Manager**: Replace `pip install` with `uv pip install` for lightning-fast installations
2. **Check Dependencies**: Use `when` conditions to install only what's needed
3. **Virtual Environments**: Always use `venv` parameter for Python packages
4. **Error Handling**: Use `next: null` to stop on errors
5. **Platform Support**: Test on all target platforms (Windows, macOS, Linux)
6. **GPU Optimization**: Support NVIDIA CUDA, AMD DirectML/ROCm, and CPU fallbacks
7. **Resource Management**: Use appropriate memory/VRAM profiles
8. **User Experience**: Provide clear menu options and status indicators
9. **Latest PyTorch**: Use PyTorch 2.7.0+ with CUDA 12.8 for best performance
10. **Optional Optimizations**: Include xformers, triton, and sageattention for advanced users

## 🚀 Installation Order Best Practices

**CRITICAL**: The order of installation steps matters! Follow this proven sequence:

### Recommended Installation Order:

```javascript
module.exports = {
  run: [
    // 1. CLONE REPOSITORIES FIRST
    {
      method: "shell.run", 
      params: {
        message: "git clone https://github.com/your-repo/project.git app"
      }
    },
    {
      method: "shell.run",
      params: {
        path: "app",
        message: "git clone https://github.com/dependency/repo.git temp_dependency"
      }
    },
    
    // 2. INSTALL ALL REQUIREMENTS (dependencies may conflict with PyTorch)
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install -r requirements.txt"
      }
    },
    {
      method: "shell.run", 
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install -r temp_dependency/requirements.txt"
      }
    },
    
    // 3. INSTALL PACKAGES IN DEVELOPMENT MODE 
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app", 
        message: "pip install -e temp_dependency/"
      }
    },
    
    // 4. INSTALL PYTORCH LAST (guarantees correct version)
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          venv: "env",
          path: "app"
        }
      }
    },
    
    // 5. VERIFY INSTALLATIONS
    {
      method: "shell.run",
      params: {
        venv: "env", 
        path: "app",
        message: "python -c \"import torch; print(f'PyTorch {torch.__version__} CUDA: {torch.cuda.is_available()}')\""
      }
    },
    
    // 6. DOWNLOAD MODELS (after all code is ready)
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "hf download model-name --local-dir models/model-name"
      }
    }
  ]
}
```

### Why This Order Works:

1. **Repositories First**: Get all source code before any installations
2. **Requirements Before PyTorch**: Let conflicting dependencies install first
3. **Development Packages**: Install local packages after their dependencies  
4. **PyTorch Last**: Guarantees final CUDA-optimized version
5. **Verification**: Confirm everything works correctly
6. **Models Last**: Download models only after environment is stable

### Common Order Mistakes:

- ❌ Installing PyTorch first (gets overwritten by requirements)
- ❌ Installing models before verifying code works
- ❌ Mixed installation order causing environment conflicts
- ❌ Installing packages in different paths (creates multiple environments)

## ⚠️ CRITICAL: Virtual Environment Management

**THE MOST IMPORTANT RULE**: Always use the **same `path` parameter** throughout your entire script!

### The Problem: Multiple Environments

```javascript
// ❌ WRONG - Creates multiple environments!
{
  method: "shell.run",
  params: {
    venv: "env",
    path: "app",           // Creates environment at: app/env/
    message: "pip install -r requirements.txt"
  }
},
{
  method: "shell.run", 
  params: {
    venv: "env",
    path: "app/subdir",    // Creates environment at: app/subdir/env/
    message: "pip install more-packages"
  }
}
```

**Result**: Two separate environments! Packages installed in `app/env/` won't be available in `app/subdir/env/`

### The Solution: Consistent Path

```javascript  
// ✅ CORRECT - Single environment!
{
  method: "shell.run",
  params: {
    venv: "env",
    path: "app",           // Uses environment: app/env/
    message: "pip install -r requirements.txt"
  }
},
{
  method: "shell.run",
  params: {
    venv: "env", 
    path: "app",           // Uses SAME environment: app/env/
    message: "pip install -r subdir/requirements.txt"  // Reference subdir files relatively
  }
}
```

### Key Rules:

1. **Environment Formula**: `path` + `venv` = Environment Location
   - `path: "app"` + `venv: "env"` = `app/env/`
   - `path: "app/temp"` + `venv: "env"` = `app/temp/env/` (DIFFERENT!)

2. **Always Use Same Path**: Pick one base path (usually `"app"`) and stick to it

3. **Reference Files Relatively**: If you need files from subdirectories, reference them from your base path:
   ```javascript
   // Install from subdirectory requirements
   message: "pip install -r subdirectory/requirements.txt"
   
   // Install package from subdirectory  
   message: "pip install -e subdirectory/"
   ```

4. **One Environment Per Project**: Don't create multiple environments unless absolutely necessary

### Common Mistakes:

- ❌ Changing `path` between commands
- ❌ Installing dependencies in different directories  
- ❌ Using `pip install -e .` in subdirectories with different paths
- ✅ Always use the same base `path` parameter
- ✅ Reference subdirectory files relatively from base path

## ⚠️ CRITICAL: PyTorch Version Conflicts

**ANOTHER CRITICAL ISSUE**: Package installations can overwrite your carefully installed PyTorch version!

### The Problem: PyTorch Gets Overwritten

```javascript
// ❌ WRONG - PyTorch gets overwritten!
{
  method: "script.start",
  params: {
    uri: "torch.js",        // Installs PyTorch 2.7.0 + CUDA 12.8
    params: { venv: "env", path: "app" }
  }
},
{
  method: "shell.run",
  params: {
    venv: "env", 
    path: "app",
    message: "pip install -r requirements.txt"  // May install torch==1.13.0!
  }
},
{
  method: "shell.run",
  params: {
    venv: "env",
    path: "app", 
    message: "pip install -e my_package/"       // May also have torch dependency!
  }
}
```

**Result**: Your CUDA-optimized PyTorch 2.7.0 gets replaced with CPU-only torch==1.13.0!

### The Enhanced Solution: Force Reinstall + No Deps

The latest torch.js implementation uses `--force-reinstall --no-deps` flags to guarantee PyTorch installation integrity:

```javascript
// ✅ ENHANCED - Force reinstall without dependency conflicts
{
  method: "shell.run",
  params: {
    venv: "env",
    path: "app", 
    message: "uv pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128 --force-reinstall --no-deps"
  }
}
```

**Why `--force-reinstall --no-deps`?**
- `--force-reinstall`: Overwrites any existing PyTorch installation, even if "satisfied"
- `--no-deps`: Prevents pip from installing unwanted dependencies that could conflict
- **Combined**: Guarantees the exact PyTorch version you want, with no interference

### The Solution: PyTorch LAST

```javascript
// ✅ CORRECT - PyTorch installed last, guaranteed final version!
{
  method: "shell.run",
  params: {
    venv: "env",
    path: "app",
    message: "pip install -r requirements.txt"  // Install all dependencies first
  }
},
{
  method: "shell.run", 
  params: {
    venv: "env",
    path: "app",
    message: "pip install -e my_package/"       // Install packages second
  }
},
{
  method: "script.start",
  params: {
    uri: "torch.js",        // Install PyTorch LAST - guaranteed final version
    params: { venv: "env", path: "app" }
  }
}
```

### Key Rules for PyTorch:

1. **Install PyTorch LAST**: Always run `torch.js` after all other pip installations
2. **Any pip install can overwrite PyTorch**: Including `pip install -r requirements.txt`, `pip install -e .`, etc.
3. **Final Installation Wins**: The last PyTorch installation determines the final version
4. **CUDA Gets Lost**: CPU-only PyTorch overwriting CUDA PyTorch breaks GPU acceleration

**Real Example from Higgs Audio V2**: The installation script follows this exact pattern - all requirements and packages are installed first, then PyTorch is installed last via `torch.js` to guarantee the correct CUDA-enabled version.

### Alternative: No-Deps Installation

```javascript
// Alternative: Prevent dependencies from overwriting PyTorch
{
  method: "shell.run",
  params: {
    venv: "env",
    path: "app",
    message: "pip install -e my_package/ --no-deps"  // Install package without dependencies
  }
}
```

But **PyTorch LAST** is the safest approach - it guarantees the correct final version.

## 🔐 HuggingFace Authentication Best Practices

**Not all HuggingFace models require authentication!** Avoid confusing users with unnecessary auth steps.

### When Authentication is Required:

1. **Gated Models**: Models requiring approval (e.g., Llama, some Stable Diffusion models)
2. **Private Models**: Models in private repositories  
3. **Commercial Models**: Models with commercial licensing restrictions

### When Authentication is NOT Required:

1. **Public Models**: Most models on HuggingFace Hub are public
2. **Open Source Models**: Models with permissive licenses (Apache, MIT, etc.)
3. **Community Models**: User-uploaded models without restrictions

### Check Before Adding Auth:

```javascript
// ❌ DON'T assume auth is needed
{
  method: "fs.write",
  params: {
    path: "app/INSTALL_COMPLETE.txt",
    text: "Installation complete!\n\n1. Authenticate with HuggingFace using 'hf auth login'"
  }
}

// ✅ DO check if models are actually gated
// Visit the model page: https://huggingface.co/username/model-name
// Look for "Gated model" or "Request access" indicators
```

### Best Practice Messages:

```javascript
// ✅ For PUBLIC models
{
  method: "fs.write", 
  params: {
    path: "app/INSTALL_COMPLETE.txt",
    text: "Installation complete!\n\nNote: All models are public and no HuggingFace authentication required.\n\nStart the application to begin!"
  }
}

// ✅ For GATED models  
{
  method: "fs.write",
  params: {
    path: "app/INSTALL_COMPLETE.txt", 
    text: "Installation complete!\n\nIMPORTANT: This project uses gated models. Please:\n1. Request access at: https://huggingface.co/model-name\n2. Run: hf auth login\n3. Enter your HuggingFace token\n\nThen start the application."
  }
}
```

### UV Package Manager Benefits

- **Speed**: 10-100x faster than traditional pip
- **Compatibility**: Drop-in replacement for pip commands
- **Reliability**: Better dependency resolution
- **Usage**: Simply prefix pip commands with `uv`: `uv pip install package`

### GPU Support Matrix

| Platform | NVIDIA | AMD | CPU |
|----------|--------|-----|-----|
| Windows | CUDA 12.8 + XFormers + Triton | DirectML | CPU-only |
| Linux | CUDA 12.8 + XFormers + SageAttention | ROCm 6.2.4 | CPU-only |
| macOS | N/A | N/A | CPU + Metal |

## Testing Your Script

1. Create the JavaScript files in your project directory
2. Add an `icon.png` file (recommended 512x512px)
3. Test installation, startup, and reset workflows
4. Verify cross-platform compatibility
5. Test with different hardware configurations

## Project Structure Template

```
your-pinokio-project/
├── pinokio.js                    # Main config with dynamic menu
├── install.js                    # Installation with proper order
├── start.js                      # Application startup with event monitoring
├── update.js                     # Smart update workflow
├── reset.js                      # Cross-platform reset
├── link.js                       # Deduplication workflow (optional)
├── torch.js                      # Advanced PyTorch installation (optional)
├── icon.png                      # Project icon
├── PINOKIO_SCRIPT_GUIDE.md       # This comprehensive guide
└── README.md                     # Project documentation
```

### Key Implementation Highlights:

1. **Dynamic Menus**: Context-aware interface with comprehensive state management
2. **Rich HTML Menus**: Professional formatting with strong text and descriptions
3. **Deduplication Support**: Optional disk space optimization via `link.js`
4. **Confirmation Dialogs**: User safety with reset confirmations
5. **Terminal Access**: Direct terminal access during running operations
6. **State Tracking**: Monitors install, start, update, reset, and link operations
7. **Generic Template**: Uses placeholders for easy customization (`<TITLE>`, `<ICON>`)
8. **User Experience**: Clear status indicators and intuitive navigation

### Advanced Menu Features Demonstrated:

- **HTML Formatting**: Rich text with `<div><strong>` tags for better presentation
- **Confirmation Prompts**: Safety measures for destructive operations
- **Multiple Running States**: Handles concurrent operation monitoring
- **Flexible Icons**: FontAwesome integration for visual appeal
- **Terminal Integration**: Direct access to running processes

This structure provides a production-ready Pinokio package template that can be easily customized for any project while maintaining professional UX standards.