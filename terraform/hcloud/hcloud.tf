provider "hcloud" {
  token = var.hcloud_token
}

resource "hcloud_firewall" "odoo_lab_firewall" {
  name = "odoo-lab-firewall"

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
  name       = "ssh-key"
  public_key = var.ssh_public_key
}

resource "hcloud_server" "web" {
  name         = var.hcloud_server_name
  image        = "ubuntu-24.04"
  server_type  = "cx23"
  location     = "nbg1"
  ssh_keys     = [hcloud_ssh_key.main.id]
  firewall_ids = [hcloud_firewall.odoo_lab_firewall.id]

  user_data = <<-EOF
    #cloud-config
    users:
      - name: deploy
        groups: sudo
        shell: /bin/bash
        sudo: ALL=(ALL) NOPASSWD:ALL
        ssh_authorized_keys:
          - ${var.ssh_public_key}
  EOF
}
