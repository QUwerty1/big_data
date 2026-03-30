using Riok.Mapperly.Abstractions;
using StorageServer.Dto;
using StorageServer.Models;

namespace StorageServer.Services;

[Mapper]
public partial class MapperService
{
    [MapperIgnoreSource(nameof(Customer.AppUser))]
    public partial CustomerDto ToDto(Customer customer);

    [MapperIgnoreTarget(nameof(Customer.AppUser))]
    public partial Customer ToEntity(CustomerDto dto);

    public partial SaleDto ToDto(Sale sale);
    public partial Sale ToEntity(SaleDto dto);

    [MapperIgnoreSource(nameof(SaleUnit.Product))]
    [MapperIgnoreSource(nameof(SaleUnit.Sales))]
    public partial SaleUnitDto ToDto(SaleUnit saleUnit);

    [MapperIgnoreTarget(nameof(SaleUnit.Product))]
    [MapperIgnoreTarget(nameof(SaleUnit.Sales))]
    public partial SaleUnit ToEntity(SaleUnitDto dto);

    [MapperIgnoreSource(nameof(Supplier.AppUser))]
    public partial SupplierDto ToDto(Supplier supplier);

    [MapperIgnoreTarget(nameof(Supplier.AppUser))]
    public partial Supplier ToEntity(SupplierDto dto);

    [MapperIgnoreSource(nameof(Supply.Supplier))]
    public partial SupplyDto ToDto(Supply supply);

    [MapperIgnoreTarget(nameof(Supply.Supplier))]
    public partial Supply ToEntity(SupplyDto dto);

    [MapperIgnoreSource(nameof(SupplyUnit.Product))]
    [MapperIgnoreSource(nameof(SupplyUnit.Supplies))]
    public partial SupplyUnitDto ToDto(SupplyUnit supplyUnit);

    [MapperIgnoreTarget(nameof(SupplyUnit.Product))]
    [MapperIgnoreTarget(nameof(SupplyUnit.Supplies))]
    public partial SupplyUnit ToEntity(SupplyUnitDto dto);

    public partial ProductDto ToDto(Product product);
    public partial Product ToEntity(ProductDto dto);

    public SaleViewDto ToViewDto(Sale sale)
    {
        return new SaleViewDto
        {
            Id = sale.Id,
            CustomerId = sale.CustomerId,
            RealDate = sale.RealDate,
            PlannedDate = sale.PlannedDate,
            SaleUnitIds = sale.SaleUnits.Select(su => su.Id).ToList()
        };
    }

    public SupplyViewDto ToViewDto(Supply supply)
    {
        return new SupplyViewDto
        {
            Id = supply.Id,
            SupplierId = supply.SupplierId,
            RealDate = supply.RealDate,
            PlannedDate = supply.PlannedDate,
            SupplyUnitIds = supply.SupplyUnits.Select(su => su.Id).ToList()
        };
    }
}