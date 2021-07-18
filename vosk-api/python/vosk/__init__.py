import os
import sys

from .vosk_cffi import ffi as _ffi

def open_dll():
    dlldir = os.path.abspath(os.path.dirname(__file__))
    if sys.platform == 'win32':
        # We want to load dependencies too
        os.environ["PATH"] = dlldir + os.pathsep + os.environ['PATH']
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(dlldir)
        return _ffi.dlopen(os.path.join(dlldir, "libvosk.dll"))
    elif sys.platform == 'linux':
        return _ffi.dlopen(os.path.join(dlldir, "libvosk.so"))
    elif sys.platform == 'darwin':
        return _ffi.dlopen(os.path.join(dlldir, "libvosk.dyld"))
    else:
        raise TypeError("Unsupported platform")

_c = open_dll()

class Model(object):

    def __init__(self, model_path):
        self._handle = _c.vosk_model_new(model_path.encode('utf-8'))

    def __del__(self):
        _c.vosk_model_free(self._handle)

    def vosk_model_find_word(self, word):
        return _c.vosk_model_find_word(self._handle, word.encode('utf-8'))

class SpkModel(object):

    def __init__(self, model_path):
        self._handle = _c.vosk_spk_model_new(model_path.encode('utf-8'))

    def __del__(self):
        _c.vosk_spk_model_free(self._handle)

class KaldiRecognizer(object):

    def __init__(self, *args):
        if len(args) == 2:
            self._handle = _c.vosk_recognizer_new(args[0]._handle, args[1])
        elif len(args) == 3 and type(args[1]) is SpkModel:
            self._handle = _c.vosk_recognizer_new_spk(args[0]._handle, args[1]._handle, args[2])
        elif len(args) == 3 and type(args[2]) is str:
            self._handle = _c.vosk_recognizer_new_grm(args[0]._handle, args[1], args[2].encode('utf-8'))
        else:
            raise TypeError("Unknown arguments")

    def __del__(self):
        _c.vosk_recognizer_free(self._handle)

    def AcceptWaveform(self, data):
        return _c.vosk_recognizer_accept_waveform(self._handle, data, len(data))

    def Result(self):
        return _ffi.string(_c.vosk_recognizer_result(self._handle)).decode('utf-8')

    def PartialResult(self):
        return _ffi.string(_c.vosk_recognizer_partial_result(self._handle)).decode('utf-8')

    def FinalResult(self):
        return _ffi.string(_c.vosk_recognizer_final_result(self._handle)).decode('utf-8')


def SetLogLevel(level):
    return _c.vosk_set_log_level(level)


def GpuInit():
    _c.vosk_gpu_init()


def GpuThreadInit():
    _c.vosk_gpu_thread_init()
