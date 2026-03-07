namespace StorageServer.Dto;

public class SupplierDto
{
    public int Id { get; set; }
    public required string CompanyName { get; set; }
    public required string Phone { get; set; }
    public required string Address { get; set; }
    public required string Email { get; set; }
    public ICollection<SupplyDto> Supplies { get; set; } = [];
    public required string AppUserId { get; set; }
}
