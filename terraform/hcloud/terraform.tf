terraform {
  cloud {
    organization = "_dev_lab_"
    workspaces {
      name = "hcloud-odoo-lab"
    }
  }

  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0"
}
