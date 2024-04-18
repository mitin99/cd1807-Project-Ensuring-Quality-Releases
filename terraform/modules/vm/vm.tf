resource "azurerm_network_interface" "main" {
  name                = "${var.application_type}-network-interface"
  location            = var.location
  resource_group_name = var.resource_group

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = var.public_ip_address_id
  }
}

resource "azurerm_linux_virtual_machine" "main" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = var.location
  resource_group_name = var.resource_group
  size                = "Standard_DS2_v2"
  admin_username      = "adminuser"
  network_interface_ids = [azurerm_network_interface.main.id]
  admin_ssh_key {
    username   = "adminuser"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC6GTz+Y/eHJ92z4z0yZE2d1NPJ6ELY1p+/Wvqa2BadRTa5byRlmADQhWSpx1xL+9GRwFy00CKWD+lzGyF5BVeAevFM2J7EU+chfsTs1pZgVEfppL7q/gy2fWP394a/WAEZixmLKzxcPEXLRyFKyx4BTANareH3xH2ZAiRtdUJ5NG3HfxjByezuLd2WxVAfJj6yZIEp5ebwnfx7WzOcizkA2wfJUZbo35lac0jSOt0qF1GDC55TXNSW8IZx/XzUc5K+5R6AlEsAuou4OfY2R9lAj4uLfBIdLFka/v+KJlwv/azsJgc2LA98rS+U1MaZBHPSTfyfODRMF+6patOnakYWfT7T5196hfIlkKjP/fLTL54u8nbwXlOkxqR8o4UENeOzrsvcLxMgSCjF+1mJF+qPvyt3PTTG/rY6f/2CKOcy0I2Ru+QqCgJCKdR1MM6HhwK3wHnKexlIQMGzhGn2uKpKqS7vByIfz9iKuCxkV2xY0MG6zAJrTNCINLKhM5ZkxOs= beoiube@LAPTOP-87BU5SMD"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

resource "azurerm_virtual_machine_extension" "main" {
  name                       = "OmsAgentForLinux"
  virtual_machine_id         = azurerm_linux_virtual_machine.main.id
  publisher                  = "Microsoft.EnterpriseCloud.Monitoring"
  type                       = "OmsAgentForLinux"
  type_handler_version       = "1.0"
  auto_upgrade_minor_version = true

   settings = <<SETTINGS
    {
        "workspaceId": "${var.log_analytics_workspace_id}"
    }
SETTINGS

  protected_settings = <<PROTECTEDSETTINGS
    {
        "workspaceKey": "${var.log_analytics_primary_shared_key}"
    }
PROTECTEDSETTINGS
}