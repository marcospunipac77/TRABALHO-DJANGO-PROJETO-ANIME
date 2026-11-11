# AniStream

Projeto acadêmico feito com Django: um catálogo de animes inspirado em serviços de streaming, sem hospedagem de episódios protegidos por direitos autorais.

## Funcionalidades

- Catálogo com busca por título/sinopse e filtro por gênero.
- Página de detalhes com temporadas, episódios, botão demonstrativo "Assistir" e link opcional para trailer.
- Cadastro e edição de animes para usuários da equipe.
- Cadastro de conta e lista de favoritos para usuários autenticados.
- Faixa de animes vistos recentemente, guardada na sessão do navegador.
- Banners gráficos originais para os títulos de demonstração.
- Django Admin para gerenciar gêneros, animes, temporadas, episódios e favoritos.

## Modelos e relacionamentos

- `Genre` se relaciona com `Anime` em muitos-para-muitos.
- `Anime` possui várias `Season`.
- `Season` possui vários `Episode`.
- `Favorite` relaciona um usuário a um anime.

## Executar no Windows

Requer Python 3.12 ou superior.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py load_demo_data
python manage.py createsuperuser
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`. O comando `load_demo_data` carrega títulos conhecidos e animes fictícios para a demonstração, com uma temporada e episódios de exemplo, e pode ser executado novamente sem duplicar os dados. Entre em `http://127.0.0.1:8000/admin/` para cadastrar gêneros, animes, temporadas e episódios. Use a conta de superusuário também para acessar os formulários de criação e edição do catálogo. Visitantes podem criar uma conta para usar a lista de favoritos.

O botão "Assistir" é apenas ilustrativo e apresenta uma mensagem de que o recurso estará disponível em breve. Os banners do catálogo são ilustrações gráficas feitas em CSS, sem imagens dos animes. Para usar outros posters, informe uma URL de imagem que você tenha permissão para usar. Os links de vídeo são opcionais e devem apontar apenas para trailers ou conteúdos autorizados.

As configurações locais usam `DEBUG=True` e uma chave de desenvolvimento. Antes de publicar o site em produção, configure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` e `DJANGO_ALLOWED_HOSTS` no ambiente do servidor; não coloque a chave secreta no GitHub.

## Testes

```powershell
python manage.py test
```

## Publicar no GitHub

Crie um repositório vazio no GitHub e, na pasta do projeto, execute:

```powershell
git init
git add .
git commit -m "Cria catálogo AniStream em Django"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```
