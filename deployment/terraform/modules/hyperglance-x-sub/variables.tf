variable "function-principal-id" {
  type        = string
  description = "The principal ID of the function"
}

variable "hyperglance-name" {
  type = string
  description = "The randomly assigned pet name"
}

variable "primary-subscription" {
  type = string
  description = "The Id of the primary subscription"
}

variable "permissions" {
  type = list(string)
  description = "List containing the permissions required for the Hyperglance role"
}