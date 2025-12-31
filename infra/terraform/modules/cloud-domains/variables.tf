variable "domain_name" {
  description = "The domain name to register (e.g. example.com)"
  type        = string
}

variable "create_domain_registration" {
  description = "Whether to create the registration"
  type        = bool
  default     = true
}

variable "name_servers" {
  description = "List of name servers from Cloud DNS"
  type        = list(string)
}

variable "yearly_price_units" {
  description = "Maximum price in USD you are willing to pay"
  type        = string
  default     = "12"
}

# Contact Params
variable "contact_name" { type = string }
variable "contact_email" { type = string }
variable "contact_phone" { type = string }
variable "contact_country_code" { type = string }
variable "contact_postal_code" { type = string }
variable "contact_state" { type = string }
variable "contact_city" { type = string }
variable "contact_address_line" { type = string }
