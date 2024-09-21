# Marketing SM

Marketing-SM is a system designed to generate and enhance social media posts for small businesses using AI. 
The application utilizes Google's Vertex AI for post generation and Pollinations AI API for image generation. 
This tool aims to assist small businesses in improving their social media presence without the need for a large 
marketing budget.

## Features

- **Content Generation**: Automatically generate Instagram posts based on business information, suggestions, and color schemes.
- **Image Generation**: Create visually appealing images based on detailed prompts.
- **Instagram Scraping**: Extract data from Instagram profiles, including captions, hashtags, and engagement metrics.
- **Business Management**: Maintain business descriptions, suggestions, Instagram profiles, and brand colors.

## Supported LLM Models

### Post Description Generation

Currently, Marketing SM supports the **Gemini 1.5 Pro** model for generating post descriptions. This model is a pay-per-use service offered by Google Cloud AI Platform. We plan to extend support to additional models in the future.

### Image Generation

Marketing SM uses the **Pollinations AI API** for image generation. This API is free to use and supports generating images based on detailed prompts. In the future, we intend to integrate additional image generation APIs or diffusion models to offer more options for image creation.

## Installation

### 1. Prerequisites

- **Google Cloud SDK**: The Google Cloud SDK must be installed on your system to interact with Google's services. You can find installation instructions [here](https://cloud.google.com/sdk/docs/install-sdk).

### 2. Clone Repository
   
Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/marketing-sm.git
   cd marketing-sm
   ```

### 3. Update Configuration Files

#### 3.1. Copy and Edit Manifest File

- Copy the template manifest file to create the actual configuration file
   ```bash
   cp marketing_sm/infrastructure/manifests/app-template.yaml marketing_sm/infrastructure/manifests/app.yaml
   ```
- Open `marketing_sm/infrastructure/manifests/app.yaml` and update the environment variables:
  - `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud application credentials file.
  - `GOOGLE_API_PROJECT`: Your Google Cloud project ID.
  - `APIFY_API_TOKEN`: Your Apify API token.
- Update the `hostPath` of the `PersistentVolume` to the absolute path of the project directory on your system.

#### 3.2. Update Tiltfile

- Open the `Tiltfile` and update the path to the Google Cloud credentials file. 
This path usually resides in the user's home directory under `.config/gcloud`. For example:
   ```bash
   # An example path (don't use this exact path):
   # "/Users/your-username/.config/gcloud/application_default_credentials.json" 
   ```

### 3.3. Create cluster (if needed)
- Execute the following command, if you need to create a development cluster to execute the service.
  ```bash
  make cluster
  ```

### 4. Installation Complete
After completing these steps, your system is set up to run the Marketing-SM service. Note that this service is still under development and not production-ready.


## Usage
To execute the service, simply use tilt:

   ```bash
   tilt up
   ```
This command will start the service in development mode, allowing you to monitor and interact with it.

## Contributing
We welcome contributions! To contribute:

1. Clone the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and add tests if applicable.
4. Submit a pull request.
Ensure your code adheres to the project's coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

We would like to extend our sincere gratitude to the following:

### [LangChain](https://python.langchain.com/)

For providing the core components of our application, including prompt templates and output parsing. 
LangChain is an open-source library that simplifies the development of applications using language models.


### [Pollinations AI](https://pollinations.ai)

For their free-to-use API for image generation. 
Pollinations AI allows us to create visually appealing content for Instagram posts without incurring additional costs.

## Community Contributions

We also appreciate the contributions and feedback from the open-source community. Your support and insights help improve the project and make it more valuable for everyone.


