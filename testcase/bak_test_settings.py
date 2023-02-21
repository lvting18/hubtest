from page.App import App


class TestSettings(object):
    @classmethod
    def setup_class(cls):
        cls.SettingsPage = App.main().gotoSettings()

    def test_gnsettings(self):
        pass