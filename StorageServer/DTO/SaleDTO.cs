namespace StorageServer.DTO;

public record SaleDTO(
    int? Id,
    int? CustomerId,
    DateTimeOffset PlannedDate,
    DateTimeOffset RealDate
    // ICollection<>
);
