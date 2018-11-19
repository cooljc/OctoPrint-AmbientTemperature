/*
 * View model for OctoPrint-AmbientTemperature
 *
 * Author: Jon Cross
 * License: AGPLv3
 */
$(function() {
    function AmbienttemperatureViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];
	self.ambiTemp = ko.observable();

	self.onDataUpdaterPluginMessage = function(plugin, data) {
		if (plugin !== "ambienttemperature") {
			return;
		}
		self.ambiTemp(_.sprintf("Ambient Temp: %.1f&deg;C", data.ambitemp));
	}
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: AmbienttemperatureViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_ambienttemperature, #tab_plugin_ambienttemperature, ...
        elements: ["#navbar_plugin_ambienttemperature" ]
    });
});
