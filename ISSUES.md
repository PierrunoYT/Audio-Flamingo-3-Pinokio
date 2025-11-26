# Known Issues and Required Fixes

## Critical Issues

### 1. Platform-Specific DeepSpeed Installation
**File:** `install.js:31`
**Issue:** Windows-specific DeepSpeed wheel installation runs on all platforms
**Impact:** Installation will fail on Linux/macOS
**Fix Needed:** Add platform detection wrapper around DeepSpeed installation
```javascript
{
  "when": "{{platform === 'win32'}}",
  method: "shell.run",
  params: {
    venv: "env",
    path: "app",
    message: "uv pip install https://github.com/6Morpheus6/deepspeed-windows-wheels/releases/download/v0.17.5/deepspeed-0.17.5+e1560d84-cp310-cp310-win_amd64.whl"
  }
}
```

### 2. Incorrect Reset Directory
**File:** `reset.js:5`
**Issue:** Resets wrong directory - removes `env` instead of `app/env`
**Impact:** Reset function doesn't work properly
**Fix Needed:** Change path to `app/env`

### 3. Git Pull Missing Path Context
**File:** `update.js:5`
**Issue:** `git pull` runs in wrong directory (should run in project root)
**Impact:** Update function may fail or update wrong repository
**Fix Needed:** Add proper path context

## Platform Compatibility Issues

### 4. CUDA Version Mismatch
**File:** `torch.js:26,88`
**Issue:** Uses cu124 but documentation claims cu128 support
**Impact:** May cause GPU compatibility issues
**Fix Needed:** Update to cu128 or correct documentation

### 5. Windows Triton Configuration
**File:** `install.js:19`
**Issue:** Triton enabled on Windows but should be Linux-only for stability
**Impact:** Potential stability issues on Windows
**Fix Needed:** Move triton to Linux-specific configuration

## Error Handling Issues

### 6. URL Regex Pattern
**File:** `start.js:18`
**Issue:** URL regex `/http:\/\/\\S+/` could match false positives
**Impact:** May incorrectly detect application startup
**Fix Needed:** Use more specific regex pattern like `/Running on (http:\/\/[^\\s]+)/`

### 7. Missing Error Handling (OPTIONAL - May not be needed)
**Files:** Various
**Issue:** No error handling for:
- Git clone failures in installation
- Model download failures
- Network connectivity issues
- Insufficient disk space
**Impact:** Users can see errors in Pinokio terminal output
**Note:** Pinokio provides terminal visibility, so extensive error handling may be unnecessary

## Minor Issues

### 8. Hardcoded Python Version
**File:** `install.js:31`
**Issue:** DeepSpeed wheel is hardcoded for Python 3.10 (cp310)
**Impact:** Will fail on other Python versions
**Fix Needed:** Detect Python version or provide fallback

### 9. Missing Dependency Verification
**Files:** All installation scripts
**Issue:** No verification that dependencies installed correctly
**Impact:** Silent failures may occur
**Fix Needed:** Add verification steps after installations

## Priority Order

1. **HIGH:** Platform-specific DeepSpeed installation
2. **HIGH:** Reset directory path fix
3. **MEDIUM:** Git pull path context
4. **MEDIUM:** CUDA version consistency
5. **LOW:** Error handling improvements
6. **LOW:** URL regex refinement

## Status

- [x] Fixed requirements.txt dependency versions
- [x] Fixed CUDA version documentation (changed from 12.8 to 12.4)
- [x] Fixed Windows Triton configuration for stability (disabled on Windows, Linux-only)
- [x] Fixed reset directory path (now removes app/env instead of entire app/ directory)
- [x] Fixed update git pull context (now runs in app/ directory)
- [x] Fixed platform-specific DeepSpeed installation (Windows wheel, Linux/macOS pip)
- [x] Improved URL detection regex (now uses more specific pattern)
- [ ] Add dependency verification steps (optional)
- [ ] Error handling (optional - may not be needed)
