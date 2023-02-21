import time
from appium.webdriver.webdriver import WebDriver
from page.App import App
import pytest
import allure
import custom_method.vpmethod as vm


class TestPreview(object):
    driver = WebDriver

    @classmethod
    def setup_class(cls):
        cls.mainPage = App.main()
        cls.mainPage.driver.maximize_window()

    def setup_method(self):
        self.mainPage = App.main()
        # self.mainPage.driver.maximize_window()

    def teardown_method(self):
        self.mainPage.driver.quit()

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ])
    def test_preview_auto_thumbnail(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        videothum = vm.yml_data["videothumb"]
        before_n = vm.get_file_number(videothum)
        vm.log().debug("number of thumbnail files before preview is "+str(before_n))
        self.mainPage.openPreview()
        time.sleep(10)
        after_n = vm.get_file_number(videothum)
        vm.log().debug("number of thumbnail files before preview is "+str(after_n))
        assert after_n > before_n

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['audio', ], ])
    def test_preview_auto_waveforms(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        audiowave = vm.yml_data["audiowave"]
        before_n = vm.get_file_number(audiowave)
        vm.log().debug("number of waveform files before preview is " + str(before_n))
        self.mainPage.openPreview()
        time.sleep(10)
        after_n = vm.get_file_number(audiowave)
        vm.log().debug("number of waveform files before preview is " + str(after_n))
        assert after_n > before_n

    @allure.feature("preview")
    def test_preview_close(self):
        self.mainPage.selectFolderFile()
        # time.sleep(2)
        self.mainPage.openPreview()
        assert self.mainPage.IsPreviewOpen()
        self.mainPage.closePreview()
        assert self.mainPage.IsPreviewClose()

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['picture', ], ])
    def test_preview_zoom(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        time.sleep(3)
        zoom_result = self.mainPage.preview_zoom()
        assert zoom_result

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['picture', ], ])
    def test_preview_rotate(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        rotate_result = self.mainPage.preview_rotate()
        assert rotate_result

    @allure.feature("preview")
    def test_preview_fullscreen(self):
        self.mainPage.selectFolderFile()
        self.mainPage.openPreview()
        time.sleep(10)
        fullscreen_result = self.mainPage.preview_fullscreen()
        assert fullscreen_result

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['picture', ], ['video', ], ])
    def test_preview_switch_files(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        result = self.mainPage.preview_switch_file()
        assert result

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ])
    def test_preview_play_video_by_space(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        time.sleep(10)
        result_space = self.mainPage.preview_play_space()
        assert result_space

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ])
    def test_preview_play_video_by_enter(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        time.sleep(10)
        result_enter = self.mainPage.preview_play_enter()
        assert result_enter

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['audio', ], ])
    def test_preview_play_audio(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        time.sleep(10)
        result_space = self.mainPage.preview_play_space()
        result_enter = self.mainPage.preview_play_enter()
        # todo: 不知道怎么assert

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ['audio', ], ])
    def test_preview_clip(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        time.sleep(10)
        result_clip = self.mainPage.preview_clip()
        assert result_clip

    @allure.feature("preview")
    @pytest.mark.parametrize(('folder_path',), [['video', ], ['audio', ], ])
    def test_preview_mute(self, folder_path):
        self.mainPage.selectFolderFile(s_path=folder_path)
        self.mainPage.openPreview()
        time.sleep(10)
        result_mute = self.mainPage.preview_mute()
        assert result_mute
