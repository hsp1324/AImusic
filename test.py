import scales as sc
import pysynth

## checking each scale


major = sc.make_scale('a', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_aMajor.wav")


major = sc.make_scale('a#', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_a#Major.wav")


major = sc.make_scale('b', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_bMajor.wav")


major = sc.make_scale('c', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_cMajor.wav")


major = sc.make_scale('c#', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_c#Major.wav")


major = sc.make_scale('d', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_dMajor.wav")


major = sc.make_scale('d#', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_d#Major.wav")


major = sc.make_scale('e', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_eMajor.wav")


major = sc.make_scale('f', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_fMajor.wav")


major = sc.make_scale('f#', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_f#Major.wav") 


major = sc.make_scale('g', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_gMajor.wav")


major = sc.make_scale('g#', 'major')
beat = [4]*7
melody = list(zip(major,beat))
pysynth.make_wav(melody, fn = "test_g#Major.wav")
