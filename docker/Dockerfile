FROM odoo:18.0
LABEL org.opencontainers.image.description="Odoo 18.0 with Worklog Module"
LABEL org.opencontainers.image.source="https://github.com/iwangub/odoo-lab"

COPY --chown=odoo:odoo addons/ /mnt/extra-addons/
COPY --chown=odoo:odoo docker/odoo.conf /etc/odoo/odoo.conf
USER odoo
