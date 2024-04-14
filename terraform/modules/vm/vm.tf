resource "azurerm_network_interface" "" {
  name                = ""
  location            = ""
  resource_group_name = ""

  ip_configuration {
    name                          = "internal"
    subnet_id                     = ""
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = ""
  }
}

resource "azurerm_linux_virtual_machine" "" {
  name                = ""
  location            = ""
  resource_group_name = ""
  size                = "Standard_DS2_v2"
  admin_username      = ""
  network_interface_ids = []
  admin_ssh_key {
    username   = "admin"
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
