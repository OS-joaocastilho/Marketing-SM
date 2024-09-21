"""
This module sets up and manages a Gradio-based user interface for handling business data and generating Instagram posts. It performs the following key functions:

1. **State Management**: Utilizes a `State` dataclass to manage and persist business information, including descriptions, Instagram profiles, and post configurations. This state is loaded from and saved to a JSON file.

2. **UI Initialization**: Creates and configures various Gradio UI components such as dropdowns, textboxes, sliders, color pickers, and buttons. These components are used for inputting and managing business data, Instagram profiles, post content, and configuration settings.

3. **Business Data Handling**:
   - **Adding and Managing Businesses**: Provides functionality to add new businesses, select existing ones, and update related data.
   - **Descriptions**: Manages business descriptions, including adding new descriptions and selecting existing ones.

4. **Instagram Profile Management**:
   - **Adding New Profiles**: Allows users to add new Instagram profiles and scrape data from them.
   - **Handling URLs**: Updates the UI based on the selected Instagram profile.

5. **Post Generation**:
   - **Creating Posts**: Generates Instagram post content based on various inputs such as business details, post type, and colors. Uses a model to create post captions and fetch related images.
   - **Configuration**: Provides sliders and inputs for configuring the number and type of posts (educational, motivational, interactive, selling) and ensures the total number of posts is accurate.

6. **UI Interaction**:
   - **Dynamic Updates**: Updates UI components dynamically based on user interactions, such as changing the number of colors or adjusting post configurations.
   - **Refresh Functionality**: Refreshes the business options and updates the UI accordingly.

7. **Launch**: Configures and starts the Gradio interface, allowing users to interact with the application through a web-based GUI.

This module integrates with various components to create a cohesive interface for managing business data and generating content, providing a complete solution for interacting with and configuring Instagram posts.
"""

import logging

from gradio_calendar import Calendar

from marketing_sm.business.model import State, Business, Description
from marketing_sm.business.ai import TextGenerationPipeline
from marketing_sm.data.scraper import scrape_instagram
from marketing_sm.presentation.language import LanguageFactory

logger = logging.getLogger()

MAX_COLORS = 6
MAX_POSTS = 12


class Interface:
    def __init__(self, gr, state: State, language: LanguageFactory):
        self.language = language
        self.state = state
        self._gr = gr

        self._posts = None
        self._output_gallery = None
        self._colors = []
        self._second_color = None
        self._third_color = None
        self._fourth_color = None
        self._fifth_color = None
        self._sixth_color = None
        self._number_colors = None
        self._principal_color = None
        self._refresh_button = None
        self._output_textbox = None
        self._generate_button = None
        self._sell_posts_input = None
        self._int_posts_input = None
        self._mot_posts_input = None
        self._edu_posts_input = None
        self._suggestions_input = None
        self._save_new_description = None
        self._description_input = None
        self._description_title = None
        self._total_posts_input = None
        self._start_date_input = None
        self._description_choice = None
        self._save_new_profile = None
        self._new_profile = None
        self._url_choice = None
        self._save_new_business = None
        self._new_business = None
        self._business_choice = None
        self._month = None

        self._business_options_orig = [self.language.add_new_brand_label]
        self.url_options_orig = {
            self.language.add_new_profile_label: Description(
                self.language.add_new_profile_label, ""
            )
        }
        self.descriptions_orig = {
            self.language.add_new_description_label: Description(
                self.language.add_new_description_label, ""
            )
        }
        self._months_dropdown = self.language.months

        self.model = TextGenerationPipeline()
        self.business_options = self._business_options_orig
        self._update_business_options()

    # BUSINESS NAME
    def new_business_change(self, option):
        new_business = option == self.language.add_new_brand_label
        url_options = self.url_options_orig.copy()
        description_options = self.descriptions_orig.copy()
        number_colors = 0
        color_updates = [self._gr.update(visible=True)] + [self._gr.update(visible=False) for _ in range(MAX_COLORS-1)]
        if not new_business and option in self.state.businesses.keys():
            business = self.state.businesses[option]
            url_options.update(business.instagram_urls)
            description_options.update(business.descriptions)
            colors = business.colors
            if not colors:
                colors = ["#000000"]
            number_colors = len([color for color in colors if color])
            color_updates = ([self._gr.update(value=color) for color in colors] +
                             [self._gr.update(visible=False) for _ in range(MAX_COLORS-number_colors)])

        return (
            self._gr.update(visible=new_business, value=""),
            self._gr.update(visible=new_business),
            self._gr.update(choices=url_options, value=""),
            self._gr.update(choices=description_options, value=""),
            self._gr.update(value=number_colors),
            *color_updates,
        )

    def save_new_business(self, business_name: str):
        if business_name not in self.business_options:
            self.state.businesses[business_name] = Business(business_name)
            self._update_business_options()
        return (
            self._gr.update(choices=self.business_options),
            self._gr.update(visible=False),
            self._gr.update(visible=False),
        )

    def _update_business_options(self):
        self.business_options = (
            list(self.state.businesses.keys()) + self._business_options_orig
        )
        self.state.store_state()

    # DESCRIPTIONS
    def new_description_change(self, business, option):
        new_description = option == self.language.add_new_description_label

        description_value = ""
        if (
            not new_description
            and business in self.state.businesses.keys()
            and option in self.state.businesses[business].descriptions
        ):
            description_value = (
                self.state.businesses[business].descriptions[option].description
            )
        return (
            self._gr.update(visible=new_description, value=""),
            self._gr.update(
                visible=True, interactive=new_description, value=description_value
            ),
            self._gr.update(visible=new_description),
        )

    def save_new_description(self, business, title, description):
        options = self.descriptions_orig.copy()
        if (
            business in self.state.businesses.keys()
            and title not in self.state.businesses[business].descriptions.keys()
        ):
            self.state.businesses[business].add_description(title, description)
            options.update(self.state.businesses[business].descriptions)
            self.state.store_state()
        return (
            self._gr.update(choices=options.keys()),
            self._gr.update(visible=True, interactive=False, value=""),
            self._gr.update(visible=False),
            self._gr.update(visible=False),
        )

    # URLs
    def new_url_change(self, option):
        visible = option == self.language.add_new_profile_label
        return self._gr.update(visible=visible), self._gr.update(visible=visible)

    def add_new_profile(self, business, url):
        options = self.url_options_orig.copy()
        if (
            business in self.state.businesses.keys()
            and url not in self.state.businesses[business].instagram_urls.keys()
        ):
            scraped_data = scrape_instagram(url)
            self.state.businesses[business].instagram_urls[url] = Description(
                url, scraped_data
            )
            options.update(self.state.businesses[business].instagram_urls)
            self.state.store_state()
        return (
            self._gr.update(choices=options.keys()),
            self._gr.update(visible=False),
            self._gr.update(visible=False),
        )

    def _create_posts(
        self,
        business,
        business_url_title,
        business_description,
        suggestions,
        month,
        total_posts,
        edu_posts,
        mot_posts,
        int_posts,
        sell_posts,
        *colors,
    ):
        found = False
        business_examples = ""
        if business in self.state.businesses.keys():
            self.state.businesses[business].save_colors(list(colors))
            self.state.store_state()
            if (
                business_url_title
                in self.state.businesses[business].instagram_urls.keys()
            ):
                business_examples = self.state.businesses[business].instagram_urls[
                    business_url_title
                ]
                found = True
        if not found:
            logger.warning(
                f"It was not possible to obtain the scraped data from {business_url_title} for business {business}"
            )

        visible_colors = [color for color in colors if color is not None]

        results = self.model.create_posts(
            business=business,
            business_examples=business_examples,
            business_description=business_description,
            suggestions=suggestions,
            month=month,
            total_posts=total_posts,
            edu_posts=edu_posts,
            mot_posts=mot_posts,
            int_posts=int_posts,
            sell_posts=sell_posts,
            colors=visible_colors,
        )
        num_posts = len(results["posts"])
        updates = []
        for idx_post in range(num_posts):
            text = self.language.post_text.format(
                results["posts"][idx_post]["post_caption"],
                results["posts"][idx_post]["prompt_image"],
            )

            images = [
                (image, results["posts"][idx_post]["caption_image"][idx])
                for idx, image in enumerate(results["posts"][idx_post]["images"])
            ]
            updates += [
                self._gr.update(visible=True),
                self._gr.update(visible=True, value=text),
                self._gr.update(visible=True, value=images),
            ]
        for idx_post in range(MAX_POSTS - num_posts):
            updates += [
                self._gr.update(visible=False),
                self._gr.update(visible=False, value=None),
                self._gr.update(visible=False, value=None),
            ]
        return updates

    def _refresh_app(self):
        self._update_business_options()
        return self._gr.update(choices=self.business_options)

    def _change_number_colors(self, number_colors):
        visible_flags = [self._gr.update(visible=True, interactive=True)] * (
            number_colors - 1
        )
        non_visible_flags = [self._gr.update(visible=False, value=None)] * (
            MAX_COLORS - number_colors
        )
        return visible_flags + non_visible_flags

    @staticmethod
    def _update_dep_sliders(total_posts, edu_posts, mot_posts, int_posts, sell_posts):
        current_total = edu_posts + mot_posts + int_posts + sell_posts
        sorted_list = sorted(
            [
                {"edu_posts": edu_posts},
                {"mot_posts": mot_posts},
                {"int_posts": int_posts},
                {"sell_posts": sell_posts},
            ],
            key=lambda x: list(x.values())[0],
        )

        while total_posts is not None and current_total < total_posts:
            key = list(sorted_list[0].keys())[0]
            sorted_list[0][key] += 1
            current_total += 1
            sorted_list = sorted(sorted_list, key=lambda x: list(x.values())[0])

        while total_posts is not None and current_total > total_posts:
            key = list(sorted_list[-1].keys())[0]
            sorted_list[-1][key] -= 1
            current_total -= 1
            sorted_list = sorted(sorted_list, key=lambda x: list(x.values())[0])

        return tuple(item[list(item.keys())[0]] for item in sorted_list)

    @staticmethod
    def _update_total_slider(edu_posts, mot_posts, int_posts, sell_posts):
        return edu_posts + mot_posts + int_posts + sell_posts

    def launch(self):
        with self._gr.Blocks() as self._demo:
            self._gr.Markdown(self.language.app_title)
            self._gr.Markdown(self.language.app_subtitle)
            self._refresh_button = self._gr.Button(self.language.refresh_button)

            with self._gr.Row():
                self._business_choice = self._gr.Dropdown(
                    label=self.language.brand_label, choices=self.business_options
                )
                self._new_business = self._gr.Textbox(
                    label=self.language.brand_name_label, visible=False
                )
                self._save_new_business = self._gr.Button(
                    self.language.new_brand_label, visible=False
                )
                self._number_colors = self._gr.Slider(
                    1, MAX_COLORS, step=1, label=self.language.colors_label
                )

            with self._gr.Row():
                self._principal_color = self._gr.ColorPicker(
                    label=self.language.main_color_label
                )
                self._second_color = self._gr.ColorPicker(
                    label=self.language.second_color_label, visible=False
                )
                self._third_color = self._gr.ColorPicker(
                    label=self.language.third_color_label, visible=False
                )
                self._fourth_color = self._gr.ColorPicker(
                    label=self.language.fourth_color_label, visible=False
                )
                self._fifth_color = self._gr.ColorPicker(
                    label=self.language.fifth_color_label, visible=False
                )
                self._sixth_color = self._gr.ColorPicker(
                    label=self.language.sixth_color_label, visible=False
                )
                self._colors = [
                    self._principal_color,
                    self._second_color,
                    self._third_color,
                    self._fourth_color,
                    self._fifth_color,
                    self._sixth_color,
                ]

            with self._gr.Row():
                self._url_choice = self._gr.Dropdown(
                    label=self.language.instagram_profile_label,
                    choices=self.url_options_orig,
                )
                self._new_profile = self._gr.Textbox(
                    label=self.language.new_instagram_profile_label, visible=False
                )
                self._save_new_profile = self._gr.Button(
                    self.language.scrape_instagram_button, visible=False
                )
                self._start_date_input = Calendar(
                    label=self.language.init_date_scrape_label
                )

                self._description_choice = self._gr.Dropdown(
                    label=self.language.page_description_label,
                    choices=self.descriptions_orig,
                )
                self._total_posts_input = self._gr.Slider(
                    1, MAX_POSTS, step=1, label=self.language.num_posts_label
                )
                self._month = self._gr.Dropdown(
                    label=self.language.posts_month_label, choices=self._months_dropdown
                )

            with self._gr.Row():
                self._description_title = self._gr.Textbox(
                    label=self.language.description_title_label, visible=False
                )
                self._description_input = self._gr.Textbox(
                    label=self.language.page_description_label,
                    lines=5,
                    visible=False,
                    interactive=False,
                )
                self._save_new_description = self._gr.Button(
                    self.language.save_description_button, visible=False
                )

            self._suggestions_input = self._gr.Textbox(
                label=self.language.input_suggestions_label, lines=3
            )

            with self._gr.Accordion(
                self.language.advanced_configurations_label, open=False
            ):
                self._edu_posts_input = self._gr.Slider(
                    0, MAX_POSTS, step=1, label=self.language.educational_posts_label
                )
                self._mot_posts_input = self._gr.Slider(
                    0, MAX_POSTS, step=1, label=self.language.motivational_posts_label
                )
                self._int_posts_input = self._gr.Slider(
                    0,
                    MAX_POSTS,
                    step=1,
                    label=self.language.interactive_posts_label,
                    value=1,
                )
                self._sell_posts_input = self._gr.Slider(
                    0, MAX_POSTS, step=1, label=self.language.selling_posts_label
                )

            self._generate_button = self._gr.Button(self.language.posts_generate_button)

            self._posts = []
            for idx in range(MAX_POSTS):
                visible = True if idx == 0 else False
                self._posts += [
                    self._gr.Markdown(f"### Post {idx + 1}", visible=visible),
                    self._gr.Textbox(
                        label=self.language.post_description_label,
                        max_lines=50,
                        lines=10,
                        visible=visible,
                    ),
                    self._gr.Gallery(
                        label=self.language.post_images_label, visible=visible
                    ),
                ]

            # BUSINESSES
            self._business_choice.change(
                self.new_business_change,
                inputs=self._business_choice,
                outputs=[
                    self._new_business,
                    self._save_new_business,
                    self._url_choice,
                    self._description_choice,
                    self._number_colors,
                    *self._colors,
                ],
            )
            self._save_new_business.click(
                self.save_new_business,
                inputs=[self._new_business],
                outputs=[
                    self._business_choice,
                    self._new_business,
                    self._save_new_business,
                ],
            )

            # COLORS
            self._number_colors.change(
                self._change_number_colors,
                inputs=[self._number_colors],
                outputs=[
                    self._second_color,
                    self._third_color,
                    self._fourth_color,
                    self._fifth_color,
                    self._sixth_color,
                ],
            )
            # DESCRIPTIONS
            self._description_choice.change(
                self.new_description_change,
                inputs=[self._business_choice, self._description_choice],
                outputs=[
                    self._description_title,
                    self._description_input,
                    self._save_new_description,
                ],
            )
            self._save_new_description.click(
                self.save_new_description,
                inputs=[
                    self._business_choice,
                    self._description_title,
                    self._description_input,
                ],
                outputs=[
                    self._description_choice,
                    self._description_input,
                    self._description_title,
                    self._save_new_description,
                ],
            )

            # URL
            self._url_choice.change(
                self.new_url_change,
                inputs=self._url_choice,
                outputs=[self._new_profile, self._save_new_profile],
            )
            self._save_new_profile.click(
                self.add_new_profile,
                inputs=[self._business_choice, self._new_profile],
                outputs=[self._url_choice, self._new_profile, self._save_new_profile],
            )

            # NUMBER POSTS
            self._total_posts_input.change(
                self._update_dep_sliders,
                inputs=[
                    self._total_posts_input,
                    self._edu_posts_input,
                    self._mot_posts_input,
                    self._int_posts_input,
                    self._sell_posts_input,
                ],
                outputs=[
                    self._edu_posts_input,
                    self._mot_posts_input,
                    self._int_posts_input,
                    self._sell_posts_input,
                ],
            )

            self._edu_posts_input.change(
                self._update_total_slider,
                inputs=[
                    self._edu_posts_input,
                    self._mot_posts_input,
                    self._int_posts_input,
                    self._sell_posts_input,
                ],
                outputs=self._total_posts_input,
            )
            self._mot_posts_input.change(
                self._update_total_slider,
                inputs=[
                    self._edu_posts_input,
                    self._mot_posts_input,
                    self._int_posts_input,
                    self._sell_posts_input,
                ],
                outputs=self._total_posts_input,
            )
            self._int_posts_input.change(
                self._update_total_slider,
                inputs=[
                    self._edu_posts_input,
                    self._mot_posts_input,
                    self._int_posts_input,
                    self._sell_posts_input,
                ],
                outputs=self._total_posts_input,
            )
            self._sell_posts_input.change(
                self._update_total_slider,
                inputs=[
                    self._edu_posts_input,
                    self._mot_posts_input,
                    self._int_posts_input,
                    self._sell_posts_input,
                ],
                outputs=self._total_posts_input,
            )
            self._generate_button.click(
                self._create_posts,
                inputs=[
                    self._business_choice,
                    self._url_choice,
                    self._description_input,
                    self._suggestions_input,
                    self._month,
                    self._total_posts_input,
                    self._edu_posts_input,
                    self._mot_posts_input,
                    self._int_posts_input,
                    self._sell_posts_input,
                    *self._colors,
                ],
                outputs=self._posts,
            )

            self._refresh_button.click(
                self._refresh_app, outputs=[self._business_choice]
            )

            logger.info("Launching the demo...")
            self._demo.launch(server_name="0.0.0.0", server_port=8000, debug=True)
