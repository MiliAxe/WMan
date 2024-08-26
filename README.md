<div align="center">

# WMan

A simple warehouse management software

</div>

## Motivation

WMan (WarehouseMan) first came into my mind when I was helping my father's business at a summer academic break.
I was tired of handling everything manually with GUI software like MS Excel. So, here is
what I came up as an effort to automize some mundane aspects of warehouse management.

## Goals

- Streamline some repeated processes in warehouse management
- Minimize human error
- Provide a CLI interface for warehouse management

## Usage

For now, you can clone the repository:
```bash
git clone https://github.com/MiliAxe/WMan.git
```

Then you can create a virtual environment and install the dependencies:
```bash
cd WMan
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

After that, you can use the module by running the following command:
```bash
python -m WMan
```

```
                                                                                                                                                                                     
 Usage: python -m WMan [OPTIONS] COMMAND [ARGS]...                                                                                                                                   
                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                                          │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation. [default: None]                   │
│ --help                                                       Show this message and exit.                                                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ availability   Manage and get availability of products                                                                                                                            │
│ customer       Manage and get information about customers                                                                                                                         │
│ order          Manage and get order information                                                                                                                                   │
│ product        Manage products and get product information                                                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Program Structure
The program is divided into 4 main parts:

### Product
This is where you can manage products and get product information. you can
add, remove, update and get product information:
```
                                                                                                                                                                                     
 Usage: python -m WMan product [OPTIONS] COMMAND [ARGS]...                                                                                                                           
                                                                                                                                                                                     
 Manage products and get product information                                                                                                                                         
                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ add            Add a new product                                                                                                                                                  │
│ add-batch      Add multiple products from a .xlsx file                                                                                                                            │
│ list           List all products or specific products                                                                                                                             │
│ remove         Delete the product with the given code                                                                                                                             │
│ update         Updates the given product with the new values                                                                                                                      │
│ update-batch   Update multiple products from a .xlsx file                                                                                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
There also exists batch operations for using .xlsx for different operations.

### Availability
This is where you can manage and get availability of products. availability refers to the amount of products available in the warehouse:

```
                                                                                                                                                                                     
 Usage: python -m WMan availability [OPTIONS] COMMAND [ARGS]...                                                                                                                      
                                                                                                                                                                                     
 Manage and get availability of products                                                                                                                                             
                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ add            Add AMOUNT to the specified product's availability                                                                                                                 │
│ add-batch      Add to the availability of the product from the specified file                                                                                                     │
│ info           Print the availability of the specified codes (separated with ,) along with other information                                                                      │
│ list           Print the availability of the products by default or output them to an .xlsx file                                                                                  │
│ reduce         Reduce AMOUNT from the specified product's availability                                                                                                            │
│ reduce-batch   Reduce the availability of the products from the specified file                                                                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Customer
This is where you can create and list customers (fow now):

```
                                                                                                                                                                                     
 Usage: python -m WMan customer [OPTIONS] COMMAND [ARGS]...                                                                                                                          
                                                                                                                                                                                     
 Manage and get information about customers                                                                                                                                          
                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create   Create a customer with the specified name.                                                                                                                               │
│ list     List all the customers with their corresponding names and IDs                                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Order
This were you can manage orders and get order information. Order refers to
the transaction of products between the warehouse and the customers. This can also create invoices (sort of):

```
                                                                                                                                                                                     
 Usage: python -m WMan order [OPTIONS] COMMAND [ARGS]...                                                                                                                             
                                                                                                                                                                                     
 Manage and get order information                                                                                                                                                    
                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ add                  Add a product to an existing order.                                                                                                                          │
│ add-batch            Add multiple products to an order from an Excel (.xlsx) file.                                                                                                │
│ add-count            Increase the quantity of a product in an existing order.                                                                                                     │
│ add-count-batch      Increase the quantities of multiple products in an order using an Excel (.xlsx) file.                                                                        │
│ create               Create a new order for a specified customer.                                                                                                                 │
│ info                 Get detailed information about a specific order.                                                                                                             │
│ list                 List orders alongside their customer, product count and total price                                                                                          │
│ reduce-count         Decrease the quantity of a product in an existing order.                                                                                                     │
│ reduce-count-batch   Decrease the quantities of multiple products in an order using an Excel (.xlsx) file.                                                                        │
│ remove               Remove a product from an existing order.                                                                                                                     │
│ remove-batch         Remove multiple products from an order using an Excel (.xlsx) file.                                                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer
This project is still in development and is not ready for production use. Use at your own risk.