---
title: "Translations"
description: "How linkding chooses the UI language and how to contribute a translation"
---

The linkding user interface is written in English and can be translated into other languages using Django's [translation framework](https://docs.djangoproject.com/en/stable/topics/i18n/translation/).

## Choosing the language

linkding picks the language from the `Accept-Language` header that the browser sends, so the user interface follows the language settings of your browser. There is no language switcher in the application.

Only languages listed in the `LANGUAGES` setting are used. If the browser requests a language that is not available, or if a text has not been translated yet, linkding falls back to English.

Currently available languages:

- English
- German

## Contributing a translation

Translations live in `bookmarks/locale/<language code>/LC_MESSAGES/django.po`. To add a new language, or to update an existing one, set up the [development environment](https://github.com/sissbruecker/linkding#development) first, then:

1. Generate or update the message file for your language. Run this from the project root:

   ```shell
   uv run manage.py makemessages -l <language code> --ignore=node_modules --ignore=.venv --ignore=static --ignore=data --ignore=docs
   ```

   For example, `uv run manage.py makemessages -l fr ...` creates `bookmarks/locale/fr/LC_MESSAGES/django.po`. When updating an existing language, the command keeps existing translations and adds new or changed texts.

2. Translate the `msgstr` entries in the `.po` file. Any text editor works, tools like [Poedit](https://poedit.net/) make this easier. Keep placeholders such as `%(count)s` and HTML tags exactly as they are in the original text.

3. If the language is new, add it to the `LANGUAGES` setting in `bookmarks/settings/base.py`.

4. Compile the translations so that they can be used by the application:

   ```shell
   uv run manage.py compilemessages --ignore .venv --ignore node_modules
   ```

   The compiled `.mo` files are not committed. When building the Docker image, they are generated automatically.

5. Start the development server with `make serve` and set your browser language to the new language to check the result.

When submitting a pull request, only include the `.po` file for your language and, for a new language, the change to the `LANGUAGES` setting.

## Notes for developers

New texts in templates need to be marked for translation using the `{% translate %}` and `{% blocktranslate %}` template tags, texts in Python code using `gettext` or `gettext_lazy`. After adding or changing texts, run `makemessages` with `-a` instead of `-l <language code>` to update all message files at once.

The few texts that are rendered by JavaScript are passed from the shared layout template to the scripts as data attributes on the `<html>` element, see `bookmarks/frontend/utils/i18n.js`.
