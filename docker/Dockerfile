FROM odoo:18.0
LABEL org.opencontainers.image.description="Odoo 18.0 with Worklog Module"
LABEL org.opencontainers.image.source="https://github.com/iwangub/odoo-lab"

COPY --chown=odoo:odoo addons/ /mnt/extra-addons/

RUN git clone --depth 1 -b 18.0 https://github.com/OCA/web /tmp/oca-web && \
    cp -r /tmp/oca-web/web_dark_mode /mnt/extra-addons/ && \
    rm -rf /tmp/oca-web \

COPY --chown=odoo:odoo docker/odoo.conf /etc/odoo/odoo.conf
USER odoo
