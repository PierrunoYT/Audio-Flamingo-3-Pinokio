Microsoft Windows [Version 10.0.26100.4652]
(c) Microsoft Corporation. Alle Rechte vorbehalten.

D:\pinokio\api\Audio-Flamingo-3-Pinokio.git\app>conda_hook && conda deactivate && conda deactivate && conda deactivate && conda activate base && D:\pinokio\api\Audio-Flamingo-3-Pinokio.git\app\env\Scripts\activate D:\pinokio\api\Audio-Flamingo-3-Pinokio.git\app\env && uv pip install -r requirements.txt
Using Python 3.10.16 environment at: env
  x Failed to build `deepspeed==0.15.4`
  |-> The build backend returned an error
  `-> Call to `setuptools.build_meta:__legacy__.build_wheel` failed (exit code: 1)

      [stdout]
      [WARNING] Unable to import torch, pre-compiling ops will be disabled. Please visit
      https://pytorch.org/ to see how to properly install torch on your system.
       [WARNING]  unable to import torch, please install it if you want to pre-compile any deepspeed
      ops.
      DS_BUILD_OPS=1

      [stderr]
      Traceback (most recent call last):
        File "<string>", line 14, in <module>
        File
      "D:\pinokio\cache\UV_CACHE_DIR\builds-v0\.tmpqg8g3i\lib\site-packages\setuptools\build_meta.py",
      line 331, in get_requires_for_build_wheel
return self._get_build_requires(config_settings, requirements=[])
        File
      "D:\pinokio\cache\UV_CACHE_DIR\builds-v0\.tmpqg8g3i\lib\site-packages\setuptools\build_meta.py",
      line 301, in _get_build_requires
self.run_setup()
        File
      "D:\pinokio\cache\UV_CACHE_DIR\builds-v0\.tmpqg8g3i\lib\site-packages\setuptools\build_meta.py",
      line 512, in run_setup
super().run_setup(setup_script=setup_script)
        File
      "D:\pinokio\cache\UV_CACHE_DIR\builds-v0\.tmpqg8g3i\lib\site-packages\setuptools\build_meta.py",
      line 317, in run_setup
exec(code, locals())
        File "<string>", line 156, in <module>
      AssertionError: Unable to pre-compile ops without torch installed. Please install torch before
      attempting to pre-compile ops.

      hint: This usually indicates a problem with the package or the build environment.

(env) (base) D:\pinokio\api\Audio-Flamingo-3-Pinokio.git\app>