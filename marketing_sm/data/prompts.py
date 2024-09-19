"""
The code sets up a system for generating Instagram content, using PromptTemplate for content creation and Pydantic
models to structure the data. It includes templates for guiding content creation and models for defining post details,
such as captions, content types, and image prompts. The JsonOutputParser ensures the generated content follows the
specified structure.
"""

from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

SYSTEM_MESSAGE = PromptTemplate.from_template(
    """
As a social media manager targeting the Portuguese market, your goal is to create effective Instagram content specifically in Portuguese of Portugal for small businesses seeking to boost their digital presence on a limited budget. The content should vary in format, including simple posts, captions, image carousels, and reels. The content strategy must include:

Educational posts: Providing really and mostly unknown valuable tips and insights.
Interactive content: Polls and quizzes to enhance engagement. Make the content interesting that generates debate.
Promotional material: Subtly showcasing products or services to generate interest.
Motivational messages: Inspirational content to connect with the audience.
To increase engagement and followers, utilize creative strategies and a range of topics, avoiding repetition. Leverage holidays and relevant events to create relatable posts. All content must be written in Portuguese of Portugal and tailored to reflect each business's unique characteristics and values. When describing images and videos, give detailed instructions to ensure visuals are accurate and aligned with the message, including specifications for colors and other elements to fit the business's identity.

{format_instructions}
"""
)

USER_MESSAGE = PromptTemplate.from_template(
    """
For the business {business} with the following description: {business_description}, create Instagram content. Here are examples of previous posts: {business_examples}.

For the month of {month}, develop a total of {total_posts} posts, distributed as follows:

{edu_posts} educational
{int_posts} interactive
{sell_posts} promotional
{mot_posts} motivational
Incorporate these suggestions into the posts: {suggestions}.

The brand colors are: {colors}. These colors must be the predominant ones in the generated images. 
They are listed in order of importance and priority, and should be used to maintain the brand's visual identity in all 
content creation.
"""
)


class Post(BaseModel):
    content_type: str = Field(
        description="Choose the type of social media content for the post, which can be a reel, an image, or a carousel. Select the format that best suits the message and resonates with the target audience, enhancing engagement and conveying the content effectively."
    )
    caption_image: List[str] = Field(
        description="Create captions that the user will incorporate directly into the images. These captions should be short, impactful, and visually appealing, as they are the primary content meant to quickly capture the audience's attention. Ensure coherence between these captions and the auxiliary information in the post_caption field. Every image must include a caption, as this is where the target content should always be placed."
    )
    post_caption: str = Field(
        description="Include a caption in the social media post description that serves as auxiliary information. Since this is not typically the main focus for most users, it should still be engaging and relevant but secondary to the captions within the images. This caption should complement the image captions, align with the overall content, and provide additional context or encourage interaction and thought without overshadowing the primary message in the images."
    )
    prompt_image: List[str] = Field(
        description="Create a detailed prompt to be sent to a diffusion model for generating a background template for the post images. The number of prompts should match the number of images in the post. For videos, ignore this field. The prompt must be extensive and rich in details, clearly specifying the colors to be used. If the colors are uncommon, replace them with similar, more common color names to avoid misinterpretation by the model. All mentioned colors should be present in the image; the first colors listed should be more prominent, while the last ones should appear only as subtle accents. Completely avoid including any text in the image. To ensure better interpretation by the model, write the prompt in English."
    )


class Posts(BaseModel):
    posts: List[Post]


OUTPUT_PARSER = JsonOutputParser(pydantic_object=Posts)
