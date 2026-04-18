variable "hcloud_token" {
  sensitive = true
}

variable "hcloud_server_name" {
  default = "odoo_lab"
}

variable "cloudflare_api_token" {
  sensitive = true
}

variable "cloudflare_zone_id" {}

variable "cloudflare_domain" {
  default = "terraform"
}
