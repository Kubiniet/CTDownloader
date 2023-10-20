import dearpygui.dearpygui as dpg

from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
from PIL import Image
import requests


dpg.create_context()

window_width = 1000
window_height = 800


def download(sender, app_data, user_data):
    video = YouTube(user_data)
    video = video.streams.get_highest_resolution()
    video.download()


def delete_cards():
    dpg.delete_item("window", children_only=True)


def show_card_video(url: str, id: int | None):
    yt = YouTube(url)
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
        with dpg.group(
            horizontal=True, tag=f"card_{id}", parent="main_menu", pos=[250, 250]
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
            button_download = dpg.add_button(
                label=f"Download {res}",
                callback=download,
                user_data=url,
                pos=[50, 380 + 200 * id],
                parent=f"card_{id}",
            )
            dpg.bind_item_font(button_download, default_font)
            dpg.bind_item_theme(button_download, "__button_theme")

    else:
        with dpg.texture_registry():
            dpg.set_value(f"image_id_{id}", data)
            dpg.set_value(f"title_video_{id}", yt.title)

    dpg.bind_item_font(f"title_video_{id}", default_font)
    dpg.bind_item_font(f"duration_video_{id}", default_font)


def check_url():
    url = dpg.get_value("input_url")
    if "list" in url:
        print("list")
        p = Playlist(url)
        delete_cards()
        for index, url in enumerate(p.video_urls):
            try:
                show_card_video(url, index)
            except VideoUnavailable:
                print(f"Video {url} is unavaialable, skipping.")
            else:
                print(f"Downloading video: {url}")

    elif "https://www.youtube.com/watch?" in url:
        try:
            show_card_video(url, id=0)
        except VideoUnavailable:
            print(f"Video {url} is unavaialable, skipping.")
        else:
            print(f"Downloading video: {url}")


dpg.create_viewport(title="Como te descargo")
dpg.configure_viewport(0, x_pos=100, y_pos=0, width=window_width, height=window_height)
dpg.set_viewport_height(window_height)
dpg.set_viewport_width(window_width)


with dpg.font_registry():
    default_font = dpg.add_font(file="fonts\Roboto\Roboto-Regular.ttf", size=30)
    custom_font = dpg.add_font(
        file="fonts\mexican-fiesta\mexican fiesta Bold.ttf", size=80
    )

# Main Window
with dpg.window(tag="main_menu") as main_menu_window:
    # Main label
    with dpg.group(horizontal=True):
        title = dpg.add_text(
            default_value="COMO TE DESCARGO",
            color=(255, 33, 0, 250),
            pos=[window_width // 2 - 280, 50],
        )
        dpg.bind_item_font(title, custom_font)
    with dpg.group(horizontal=True):
        input = dpg.add_input_text(
            default_value="url", tag="input_url", height=50, width=800, pos=[50, 200]
        )
        dpg.bind_item_font(input, default_font)
        button_search = dpg.add_button(label="Search", callback=check_url)
        dpg.bind_item_font(button_search, default_font)

        with dpg.theme(tag="__button_theme"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 35, 0, 250))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (51, 51, 55))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (37, 37, 38))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 3)

        dpg.bind_item_theme(button_search, "__button_theme")


dpg.set_primary_window(window=main_menu_window, value=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
