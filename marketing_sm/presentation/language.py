"""
This module defines an abstract base class `LanguageFactory` and its concrete implementation `PortugueseLanguage` for managing language-specific text in a Gradio-based application.

### `LanguageFactory` (Abstract Base Class)
The `LanguageFactory` class serves as an abstract base class for creating language-specific text resources. It defines a set of properties that subclasses must implement, each representing a specific text element used in the user interface.
"""

from abc import ABC, abstractmethod
from typing import List


class LanguageFactory(ABC):
    @property
    @abstractmethod
    def months(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def add_new_brand_label(self) -> str:
        pass

    @property
    @abstractmethod
    def add_new_description_label(self) -> str:
        pass

    @property
    @abstractmethod
    def add_new_profile_label(self) -> str:
        pass

    @property
    @abstractmethod
    def post_text(self) -> str:
        pass

    @property
    @abstractmethod
    def app_title(self) -> str:
        pass

    @property
    @abstractmethod
    def app_subtitle(self) -> str:
        pass

    @property
    @abstractmethod
    def refresh_button(self) -> str:
        pass

    @property
    @abstractmethod
    def brand_label(self) -> str:
        pass

    @property
    @abstractmethod
    def brand_name_label(self) -> str:
        pass

    @property
    @abstractmethod
    def new_brand_label(self) -> str:
        pass

    @property
    @abstractmethod
    def colors_label(self) -> str:
        pass

    @property
    @abstractmethod
    def main_color_label(self) -> str:
        pass

    @property
    @abstractmethod
    def second_color_label(self) -> str:
        pass

    @property
    @abstractmethod
    def third_color_label(self) -> str:
        pass

    @property
    @abstractmethod
    def fourth_color_label(self) -> str:
        pass

    @property
    @abstractmethod
    def fifth_color_label(self) -> str:
        pass

    @property
    @abstractmethod
    def sixth_color_label(self) -> str:
        pass

    @property
    @abstractmethod
    def instagram_profile_label(self) -> str:
        pass

    @property
    @abstractmethod
    def new_instagram_profile_label(self) -> str:
        pass

    @property
    @abstractmethod
    def scrape_instagram_button(self) -> str:
        pass

    @property
    @abstractmethod
    def init_date_scrape_label(self) -> str:
        pass

    @property
    @abstractmethod
    def page_description_label(self) -> str:
        pass

    @property
    @abstractmethod
    def num_posts_label(self) -> str:
        pass

    @property
    @abstractmethod
    def posts_month_label(self) -> str:
        pass

    @property
    @abstractmethod
    def description_title_label(self) -> str:
        pass

    @property
    @abstractmethod
    def save_description_button(self) -> str:
        pass

    @property
    @abstractmethod
    def input_suggestions_label(self) -> str:
        pass

    @property
    @abstractmethod
    def advanced_configurations_label(self) -> str:
        pass

    @property
    @abstractmethod
    def educational_posts_label(self) -> str:
        pass

    @property
    @abstractmethod
    def motivational_posts_label(self) -> str:
        pass

    @property
    @abstractmethod
    def interactive_posts_label(self) -> str:
        pass

    @property
    @abstractmethod
    def selling_posts_label(self) -> str:
        pass

    @property
    @abstractmethod
    def posts_generate_button(self) -> str:
        pass

    @property
    @abstractmethod
    def post_description_label(self) -> str:
        pass

    @property
    @abstractmethod
    def post_images_label(self) -> str:
        pass


class PortugueseLanguage(LanguageFactory):

    @property
    def post_images_label(self) -> str:
        return "Imagens"

    @property
    def post_description_label(self) -> str:
        return "Descrição"

    @property
    def posts_generate_button(self) -> str:
        return "Gerar Posts"

    @property
    def selling_posts_label(self) -> str:
        return "Posts de Venda"

    @property
    def interactive_posts_label(self) -> str:
        return "Posts Interactivos"

    @property
    def motivational_posts_label(self) -> str:
        return "Posts Motivacionais"

    @property
    def educational_posts_label(self) -> str:
        return "Posts Educacionais"

    @property
    def advanced_configurations_label(self) -> str:
        return "⚙️ Configurações Avançadas"

    @property
    def input_suggestions_label(self) -> str:
        return "Sugestões sobre os Posts"

    @property
    def save_description_button(self) -> str:
        return "Guardar Descrição"

    @property
    def description_title_label(self) -> str:
        return "Titulo da Descrição"

    @property
    def posts_month_label(self) -> str:
        return "Mês dos Posts"

    @property
    def num_posts_label(self) -> str:
        return "Quantos Posts são pretendidos?"

    @property
    def page_description_label(self) -> str:
        return "Descrição da Página"

    @property
    def init_date_scrape_label(self) -> str:
        return "Início da Leitura do Instagram"

    @property
    def scrape_instagram_button(self) -> str:
        return "Ler Perfil de Instagram"

    @property
    def new_instagram_profile_label(self) -> str:
        return "Novo Perfil de Instagram (URL)"

    @property
    def instagram_profile_label(self) -> str:
        return "Perfil de Instagram"

    @property
    def sixth_color_label(self) -> str:
        return "Outra Cor (Sexta)"

    @property
    def fifth_color_label(self) -> str:
        return "Outra Cor (Quinta)"

    @property
    def fourth_color_label(self) -> str:
        return "Outra Cor (Quarta)"

    @property
    def third_color_label(self) -> str:
        return "Outra Cor (Terceira)"

    @property
    def second_color_label(self) -> str:
        return "Cor Secundária"

    @property
    def main_color_label(self) -> str:
        return "Cor Principal"

    @property
    def colors_label(self) -> str:
        return "Quantas cores identificam a marca?"

    @property
    def new_brand_label(self) -> str:
        return "Nova Marca"

    @property
    def brand_name_label(self) -> str:
        return "Nome da Marca"

    @property
    def brand_label(self) -> str:
        return "Marca"

    @property
    def refresh_button(self) -> str:
        return "Atualizar"

    @property
    def app_subtitle(self) -> str:
        return "### Gere posts para o Instagram com facilidade usando IA"

    @property
    def app_title(self) -> str:
        return "# 🧠 AI Geração de Posts Instagram"

    @property
    def post_text(self) -> str:
        return """
            Descrição: {}

            Prompt para a imagem (caso pretenda usar outro modelo): {}
        """

    @property
    def add_new_profile_label(self) -> str:
        return "Adicionar Novo Perfil"

    @property
    def add_new_description_label(self) -> str:
        return "Adicionar Nova Descrição"

    @property
    def add_new_brand_label(self) -> str:
        return "Adicionar Nova Marca"

    @property
    def months(self) -> List[str]:
        return [
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]
