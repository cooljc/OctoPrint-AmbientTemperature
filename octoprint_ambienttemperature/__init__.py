# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
from octoprint.util import RepeatedTimer
from octoprint_ambienttemperature.temper import Temper


class AmbienttemperaturePlugin(octoprint.plugin.StartupPlugin,
                               octoprint.plugin.SettingsPlugin,
                               octoprint.plugin.AssetPlugin,
                               octoprint.plugin.TemplatePlugin):

        def __init__(self):
            self.displayTemp = True
            self._checkTempTimer = None
            self.temper = None

        ##~~ SettingsPlugin mixin

        def on_after_startup(self):
            #self.temper = Temper()
            #if len(self.temper.devices) > 0:
            #    self._logger.info("Found TEMPer device")
            self.startTimer(15.0)

        def startTimer(self, interval):
            self._checkTempTimer = RepeatedTimer(interval, self.checkTemp, None, None, True)
            self._checkTempTimer.start()

        def checkTemp(self):
            temper = Temper()
            if len(temper.devices) > 0:
                temp = temper.getTemperature(temper.devices[0])
                #self._logger.info("Temperature: %s" % temp)
                self._plugin_manager.send_plugin_message(self._identifier, dict(ambitemp=temp))

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/ambienttemperature.js"],
			css=["css/ambienttemperature.css"],
			less=["less/ambienttemperature.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			ambienttemperature=dict(
				displayName="Ambienttemperature Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="cooljc",
				repo="OctoPrint-AmbientTemperature",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/cooljc/OctoPrint-AmbientTemperature/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Ambienttemperature Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = AmbienttemperaturePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

