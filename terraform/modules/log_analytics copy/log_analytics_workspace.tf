data "azurerm_log_analytics_workspace" "main" {
  name                = "my-first-log"
  resource_group_name = var.resource_group_name
}
