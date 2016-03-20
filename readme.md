Tiny Hands PAC
==================

The initial foundation of this project came from https://github.com/chrisdev/wagtail-cookiecutter-foundation with some terrible modifications because Donald Trump is a terrible human. Detailed setup instructions can be found at the link.

The code in this repo needs to be run to generate a static version of the website. Despite the craziness of the idea, the repo also includes the site database, so multiple people can work (locally) off the same base of content. To update the website, follow the instructions for getting the site running locally; follow the instructions for exporting a static copy of the site; then copy over the resulting files into the website's github repository.

If we have more time, it would be lovely to clean this process up significantly.

Running locally
--

1. Ensure you've got these things:
 - pip
 - virtualenv/pyvenv/virtualenvwrapper
 - node, npm and git and bower

2. Download this repo

3. `make virtualenv`

4. `make requirements`

5. `./manage.py runserver`

6. That should be all you need to do. The database is already build and included. Wagtail is accessible at `/admin/` with u/p admin/admin.

Deploying
--

The site is hosted with Github and needs to be exported to static files. Fortunately, it's all rolled up into a single command:

1. `make static_site`

Running this command will install the necessary packages, compress the specified CSS and Javascript, generate HTML pages, collect static assets, and everything into a single directory (`static_build`) which can then be "deployed" as needed.
