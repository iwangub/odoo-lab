variable "hcloud_token" {
  sensitive = true
}

variable "odoo_version" {}

provider "hcloud" {
  token = var.hcloud_token
}

resource "hcloud_firewall" "odoo_firewall" {
  name = "odoo-lab"

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "22"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "80"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "443"
    source_ips = ["0.0.0.0/0", "::/0"]
  }
}

resource "hcloud_ssh_key" "main" {
  name = "ssh-key"
  public_key = file("~/.ssh/id_ed25519.pub")
}

resource "hcloud_server" "web" {
  name         = "odoo-${var.odoo_version}"
  image        = "ubuntu-24.04"
  server_type  = "cx23"
  location     = "nbg1"
  ssh_keys     = [hcloud_ssh_key.main.id]
  firewall_ids = [hcloud_firewall.odoo_firewall.id]
}

output "server_ip" {
  value = hcloud_server.web.ipv4_address
}
