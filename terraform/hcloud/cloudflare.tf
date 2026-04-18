provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

resource "cloudflare_record" "odoo_lab_record" {
  zone_id = var.cloudflare_zone_id
  name    = var.cloudflare_domain
  content = hcloud_server.web.ipv4_address
  type    = "A"
  proxied = false
}
