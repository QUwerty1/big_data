using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

using StorageServer.Dto;
using StorageServer.Services;

namespace StorageServer.Controllers;

[Route("generator")]
[ApiController]
[Authorize(Policy = "IsStaff")]
public class GeneratorController(
    GeneratorService generatorService,
    MapperService mapperService
) : ControllerBase
{
    private readonly GeneratorService _generatorService = generatorService;
    private readonly MapperService _mapperService = mapperService;

    [HttpPost("users")]
    [ProducesResponseType<string[]>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GenerateUsers([FromQuery] int count = 1)
    {
        if (count < 1)
            return BadRequest();

        var users = await _generatorService.GenerateUsersAsync(count);

        return Ok(users.Select(u => u.UserName));
    }

    [HttpPost("customers")]
    [ProducesResponseType<CustomerDto[]>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GenerateCustomers([FromQuery] int count = 1)
    {
        if (count < 1)
            return BadRequest();

        var customers =
            await _generatorService.GenerateCustomerAsync(count);

        return Ok(customers.Select(_mapperService.ToDto));
    }

    [HttpPost("suppliers")]
    [ProducesResponseType<SupplierDto[]>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GenerateSuppliers([FromQuery] int count = 1)
    {
        if (count < 1)
            return BadRequest();

        var suppliers =
            await _generatorService.GenerateSupplierAsync(count);

        return Ok(suppliers.Select(_mapperService.ToDto));
    }

    [HttpPost("products")]
    [ProducesResponseType<ProductDto[]>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GenerateProductsInRange(
        [FromQuery] int count = 1,
        [FromQuery] decimal minPrice = 1,
        [FromQuery] decimal maxPrice = 50_000
    )
    {
        if (count < 1 || minPrice < 0 || maxPrice < minPrice)
            return BadRequest();

        var products =
            await _generatorService.GenerateProductAsync(count, minPrice, maxPrice);

        return Ok(products.Select(_mapperService.ToDto));
    }

    [HttpPost("sales")]
    [ProducesResponseType<SaleDto[]>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GenerateSales(
        [FromQuery] DateTimeOffset minDate,
        [FromQuery] DateTimeOffset maxDate,
        [FromQuery] int count = 1
    )
    {
        if (count < 1)
            return BadRequest();

        var sales = await _generatorService.GenerateSalesAsync(minDate, maxDate, count);
        return Ok(sales.Select(_mapperService.ToDto));
    }

    [HttpPost("supplies")]
    [ProducesResponseType<SupplyDto[]>(StatusCodes.Status200OK)]
    public async Task<IActionResult> GenerateSupplies(
        [FromQuery] DateTimeOffset minDate,
        [FromQuery] DateTimeOffset maxDate,
        [FromQuery] int count = 1
    )
    {
        if (count < 1)
            return BadRequest();

        var supplies = await _generatorService.GenerateSuppliesAsync(minDate, maxDate, count);
        return Ok(supplies.Select(_mapperService.ToDto));
    }
}
