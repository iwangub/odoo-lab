output "server_ip" {
  value = hcloud_server.web.ipv4_address
}

output "dns" {
  value = "https://${var.cloudflare_domain}.dev-lab.dev"
}

output "dns_domain" {
  value = "${var.cloudflare_domain}.dev-lab.dev"
}
