FROM alpine/git AS oca
RUN git clone --depth 1 -b 18.0 https://github.com/OCA/web /oca-web

FROM odoo:18.0
LABEL org.opencontainers.image.description="Odoo 18.0 with Worklog Module"
LABEL org.opencontainers.image.source="https://github.com/iwangub/odoo-lab"

COPY --chown=odoo:odoo --from=oca /oca-web/web_dark_mode /mnt/extra-addons/web_dark_mode
COPY --chown=odoo:odoo addons/ /mnt/extra-addons/

COPY --chown=odoo:odoo docker/odoo.conf /etc/odoo/odoo.conf
USER odoo
