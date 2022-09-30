import os
from pedalboard import Pedalboard, Reverb, load_plugin
from pedalboard.io import AudioFile

class VSTHost:

    def __init__(self, vst_path):
        self.vst_path = vst_path
        self.vst = load_plugin(vst_path)

    def apply_settings(self, settings):
        for key, value in settings.items():
            setattr(self.vst, key, value)            

    def print_parameters(self):
        for key, val in self.vst.parameters.items():
            print(key, val)

    def render(self, audio, samplerate):
        return self.vst(audio, samplerate)


def get_vsts():
    # load gojira delay
    gojira_delay = VSTHost("C:\Program Files\Common Files\VST3\\Neural DSP\Archetype Gojira.vst3")
    gojira_delay.apply_settings({
        "amp_section_active": "Inactive",
        "cab_section_active": "Inactive",
        "dly_active": "Active",
        "dly_sync_active": "Inactive",
        "dly_dry_wet": 0.5,
    })

    # load gojira shimmer reverb
    gojira_shimmer = VSTHost("C:\Program Files\Common Files\VST3\\Neural DSP\Archetype Gojira.vst3")
    gojira_shimmer.apply_settings({
        "amp_section_active": "Inactive",
        "cab_section_active": "Inactive",
        "rev_active": "Active",
        "rev_dry_wet": 0.5,
        "rev_mode": "Shimmer"
    })
    return gojira_delay, gojira_shimmer


