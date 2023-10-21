import dearpygui.dearpygui as dpg

from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
from PIL import Image
import requests


dpg.create_context()

window_width = 1000
window_height = 800


def download_mp4(sender, app_data, user_data):
    video = YouTube(user_data)
    video = video.streams.get_highest_resolution()
    video.download()


def download_mp3(sender, app_data, user_data):
    video = YouTube(user_data)
    stream = video.streams.filter(only_audio=True).first()
    stream.download(filename=f"{video.title}.mp3")


def delete_cards():
    dpg.delete_item("cards_container", children_only=True)


def show_card_video(url: str, id: int | None):
    yt = YouTube(url)
    try:
        yt.check_availability()
        response = requests.get(yt.thumbnail_url)
        res = yt.streams.get_highest_resolution().resolution

        with open(f"image_{id}.jpg", "wb") as f:
            f.write(response.content)
        img = Image.open(f"image_{id}.jpg")
        img_resized = img.resize((320, 180))
        img_resized.save(f"image_{id}.jpg")
        width, height, channels, data = dpg.load_image(f"image_{id}.jpg")
        if not dpg.get_item_alias(f"image_id_{id}"):
            with dpg.texture_registry():
                dpg.add_dynamic_texture(width, height, data, tag=f"image_id_{id}")
        else:
            dpg.set_value(f"image_id_{id}", data)
        with dpg.group(
            horizontal=True,
            tag=f"card_{id}",
            parent="cards_container",
            pos=[250, 250],
        ):
            dpg.add_text(
                f"{yt.title} {yt.length//60}:{yt.length%60}",
                tag=f"title_video_{id}",
                pos=[50, 250 + 200 * id],
                wrap=580,
                parent=f"card_{id}",
            )
            dpg.add_text(
                f"{yt.length//60}:{yt.length%60}",
                tag=f"duration_video_{id}",
                pos=[50, 300 + 200 * id],
                show=False,
                parent=f"card_{id}",
            )
            dpg.add_image(
                f"image_id_{id}",
                pos=[window_width - 50 - width, 250 + 200 * id],
                parent=f"card_{id}",
            )
            dpg.add_text(
                "Download",
                tag=f"download_label_{id}",
                parent=f"card_{id}",
                pos=[50, 380 + 200 * id],
            )
            download_video = dpg.add_button(
                label=f"{res} mp4",
                callback=download_mp4,
                user_data=url,
                pos=[200, 380 + 200 * id],
                parent=f"card_{id}",
            )
            download_audio = dpg.add_button(
                label=f"mp3",
                callback=download_mp3,
                user_data=url,
                pos=[350, 380 + 200 * id],
                parent=f"card_{id}",
            )
            dpg.bind_item_font(download_audio, default_font)
            dpg.bind_item_theme(download_audio, "__button_theme_blue")
            dpg.bind_item_font(download_video, default_font)
            dpg.bind_item_theme(download_video, "__button_theme")
            dpg.bind_item_font(f"title_video_{id}", default_font)
            dpg.bind_item_font(f"duration_video_{id}", default_font)
            dpg.bind_item_font(f"download_label_{id}", default_font)
    except Exception as e:
        print(e)
        with dpg.group(
            horizontal=True, tag=f"card_{id}", parent="cards_container", pos=[250, 250]
        ):
            dpg.add_text(
                f"{yt.title} {yt.length//60}:{yt.length%60}",
                tag=f"title_video_{id}",
                pos=[50, 250 + 200 * id],
                wrap=580,
                parent=f"card_{id}",
            )
            dpg.add_text(
                f"Video is unavaliable",
                tag=f"no_video_{id}",
                pos=[50, 280 + 200 * id],
                wrap=580,
                parent=f"card_{id}",
            )
            dpg.bind_item_font(f"title_video_{id}", default_font)
            dpg.bind_item_font(f"no_video_{id}", default_font)


def check_url():
    delete_cards()
    url = dpg.get_value("input_url")
    if "list" in url:
        p = Playlist(url)
        for index, url in enumerate(p.video_urls):
            show_card_video(url, index)
    elif "https://www.youtube.com/watch?" in url:
        show_card_video(url, id=0)


dpg.create_viewport(title="Como te descargo")
dpg.configure_viewport(0, x_pos=100, y_pos=0, width=window_width, height=window_height)
dpg.set_viewport_height(window_height)
dpg.set_viewport_width(window_width)


with dpg.font_registry():
    default_font = dpg.add_font(file="fonts\Roboto\Roboto-Regular.ttf", size=30)
    custom_font = dpg.add_font(
        file="fonts\mexican-fiesta\mexican fiesta Bold.ttf", size=80
    )
with dpg.theme(tag="__button_theme_blue"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (78, 174, 215))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (51, 51, 55))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (37, 37, 38))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 3)

with dpg.theme(tag="__button_theme"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 35, 0, 250))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (51, 51, 55))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (37, 37, 38))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 3)


with dpg.window(tag="main_menu") as main_menu_window:
    """Main Window"""
    with dpg.group(horizontal=True):
        title = dpg.add_text(
            default_value="COMO TE DESCARGO",
            pos=[window_width // 2 - 280, 50],
        )
        dpg.bind_item_font(title, custom_font)

    with dpg.group(horizontal=True):
        """Input of url and button search"""
        input = dpg.add_input_text(
            default_value="url", tag="input_url", height=50, width=800, pos=[50, 200]
        )
        dpg.bind_item_font(input, default_font)
        button_search = dpg.add_button(label="Search", callback=check_url)
        dpg.bind_item_font(button_search, default_font)

        dpg.bind_item_theme(button_search, "__button_theme")
    dpg.add_group(tag="cards_container", parent="main_menu")


dpg.set_primary_window(window=main_menu_window, value=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
