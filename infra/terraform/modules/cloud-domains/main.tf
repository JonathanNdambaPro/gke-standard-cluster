resource "google_clouddomains_registration" "my_domain" { # WARNING: can't be destroy it's just abandonned have to be donne manually with CLI or UI
  count       = var.create_domain_registration ? 1 : 0    # If already exist donn't try to create
  domain_name = var.domain_name
  location    = "global"

  yearly_price {
    currency_code = "USD"
    units         = var.yearly_price_units # Max price you are willing to pay (e.g. 12.00)
  }

  dns_settings {
    custom_dns {
      name_servers = var.name_servers
    }
  }

  contact_settings {
    privacy = "REDACTED_CONTACT_DATA" # Masque les données WHOIS

    registrant_contact {
      phone_number = var.contact_phone
      email        = var.contact_email
      postal_address {
        region_code         = var.contact_country_code # "US", "FR"
        postal_code         = var.contact_postal_code
        administrative_area = var.contact_state # "CA", "Ile-de-France"
        locality            = var.contact_city
        address_lines       = [var.contact_address_line]
        recipients          = [var.contact_name]
      }
    }

    admin_contact {
      phone_number = var.contact_phone
      email        = var.contact_email
      postal_address {
        region_code         = var.contact_country_code
        postal_code         = var.contact_postal_code
        administrative_area = var.contact_state
        locality            = var.contact_city
        address_lines       = [var.contact_address_line]
        recipients          = [var.contact_name]
      }
    }

    technical_contact {
      phone_number = var.contact_phone
      email        = var.contact_email
      postal_address {
        region_code         = var.contact_country_code
        postal_code         = var.contact_postal_code
        administrative_area = var.contact_state
        locality            = var.contact_city
        address_lines       = [var.contact_address_line]
        recipients          = [var.contact_name]
      }
    }
  }
}
