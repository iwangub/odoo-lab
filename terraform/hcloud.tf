variable "hcloud_token" {
  sensitive = true
}

variable "odoo_version" {}

provider "hcloud" {
  token = var.hcloud_token
}

resource "hcloud_server" "web" {
  name        = "odoo-${var.odoo_version}"
  image       = "ubuntu-24.04"
  server_type = "cx22"
}
