using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace StorageServer.Migrations
{
    /// <inheritdoc />
    public partial class AddRemainingModelsDbSets : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Supplier_AppUser_AppUserId",
                table: "Supplier");

            migrationBuilder.DropForeignKey(
                name: "FK_Supply_Supplier_SupplierId",
                table: "Supply");

            migrationBuilder.DropForeignKey(
                name: "FK_SupplySupplyUnit_SupplyUnit_SupplyUnitsId",
                table: "SupplySupplyUnit");

            migrationBuilder.DropForeignKey(
                name: "FK_SupplySupplyUnit_Supply_SuppliesId",
                table: "SupplySupplyUnit");

            migrationBuilder.DropForeignKey(
                name: "FK_SupplyUnit_Products_ProductId",
                table: "SupplyUnit");

            migrationBuilder.DropPrimaryKey(
                name: "PK_SupplyUnit",
                table: "SupplyUnit");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Supply",
                table: "Supply");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Supplier",
                table: "Supplier");

            migrationBuilder.RenameTable(
                name: "SupplyUnit",
                newName: "SupplyUnits");

            migrationBuilder.RenameTable(
                name: "Supply",
                newName: "Supplies");

            migrationBuilder.RenameTable(
                name: "Supplier",
                newName: "Suppliers");

            migrationBuilder.RenameIndex(
                name: "IX_SupplyUnit_ProductId",
                table: "SupplyUnits",
                newName: "IX_SupplyUnits_ProductId");

            migrationBuilder.RenameIndex(
                name: "IX_Supply_SupplierId",
                table: "Supplies",
                newName: "IX_Supplies_SupplierId");

            migrationBuilder.RenameIndex(
                name: "IX_Supplier_AppUserId",
                table: "Suppliers",
                newName: "IX_Suppliers_AppUserId");

            migrationBuilder.AlterColumn<string>(
                name: "Phone",
                table: "Suppliers",
                type: "nvarchar(16)",
                maxLength: 16,
                nullable: false,
                defaultValue: "",
                oldClrType: typeof(string),
                oldType: "nvarchar(16)",
                oldMaxLength: 16,
                oldNullable: true);

            migrationBuilder.AlterColumn<string>(
                name: "Email",
                table: "Suppliers",
                type: "nvarchar(30)",
                maxLength: 30,
                nullable: false,
                defaultValue: "",
                oldClrType: typeof(string),
                oldType: "nvarchar(30)",
                oldMaxLength: 30,
                oldNullable: true);

            migrationBuilder.AlterColumn<string>(
                name: "Address",
                table: "Suppliers",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "",
                oldClrType: typeof(string),
                oldType: "nvarchar(max)",
                oldNullable: true);

            migrationBuilder.AddPrimaryKey(
                name: "PK_SupplyUnits",
                table: "SupplyUnits",
                column: "Id");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Supplies",
                table: "Supplies",
                column: "Id");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Suppliers",
                table: "Suppliers",
                column: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_Suppliers_AppUser_AppUserId",
                table: "Suppliers",
                column: "AppUserId",
                principalTable: "AppUser",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Supplies_Suppliers_SupplierId",
                table: "Supplies",
                column: "SupplierId",
                principalTable: "Suppliers",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_SupplySupplyUnit_Supplies_SuppliesId",
                table: "SupplySupplyUnit",
                column: "SuppliesId",
                principalTable: "Supplies",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_SupplySupplyUnit_SupplyUnits_SupplyUnitsId",
                table: "SupplySupplyUnit",
                column: "SupplyUnitsId",
                principalTable: "SupplyUnits",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_SupplyUnits_Products_ProductId",
                table: "SupplyUnits",
                column: "ProductId",
                principalTable: "Products",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Suppliers_AppUser_AppUserId",
                table: "Suppliers");

            migrationBuilder.DropForeignKey(
                name: "FK_Supplies_Suppliers_SupplierId",
                table: "Supplies");

            migrationBuilder.DropForeignKey(
                name: "FK_SupplySupplyUnit_Supplies_SuppliesId",
                table: "SupplySupplyUnit");

            migrationBuilder.DropForeignKey(
                name: "FK_SupplySupplyUnit_SupplyUnits_SupplyUnitsId",
                table: "SupplySupplyUnit");

            migrationBuilder.DropForeignKey(
                name: "FK_SupplyUnits_Products_ProductId",
                table: "SupplyUnits");

            migrationBuilder.DropPrimaryKey(
                name: "PK_SupplyUnits",
                table: "SupplyUnits");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Supplies",
                table: "Supplies");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Suppliers",
                table: "Suppliers");

            migrationBuilder.RenameTable(
                name: "SupplyUnits",
                newName: "SupplyUnit");

            migrationBuilder.RenameTable(
                name: "Supplies",
                newName: "Supply");

            migrationBuilder.RenameTable(
                name: "Suppliers",
                newName: "Supplier");

            migrationBuilder.RenameIndex(
                name: "IX_SupplyUnits_ProductId",
                table: "SupplyUnit",
                newName: "IX_SupplyUnit_ProductId");

            migrationBuilder.RenameIndex(
                name: "IX_Supplies_SupplierId",
                table: "Supply",
                newName: "IX_Supply_SupplierId");

            migrationBuilder.RenameIndex(
                name: "IX_Suppliers_AppUserId",
                table: "Supplier",
                newName: "IX_Supplier_AppUserId");

            migrationBuilder.AlterColumn<string>(
                name: "Phone",
                table: "Supplier",
                type: "nvarchar(16)",
                maxLength: 16,
                nullable: true,
                oldClrType: typeof(string),
                oldType: "nvarchar(16)",
                oldMaxLength: 16);

            migrationBuilder.AlterColumn<string>(
                name: "Email",
                table: "Supplier",
                type: "nvarchar(30)",
                maxLength: 30,
                nullable: true,
                oldClrType: typeof(string),
                oldType: "nvarchar(30)",
                oldMaxLength: 30);

            migrationBuilder.AlterColumn<string>(
                name: "Address",
                table: "Supplier",
                type: "nvarchar(max)",
                nullable: true,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AddPrimaryKey(
                name: "PK_SupplyUnit",
                table: "SupplyUnit",
                column: "Id");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Supply",
                table: "Supply",
                column: "Id");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Supplier",
                table: "Supplier",
                column: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_Supplier_AppUser_AppUserId",
                table: "Supplier",
                column: "AppUserId",
                principalTable: "AppUser",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Supply_Supplier_SupplierId",
                table: "Supply",
                column: "SupplierId",
                principalTable: "Supplier",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_SupplySupplyUnit_SupplyUnit_SupplyUnitsId",
                table: "SupplySupplyUnit",
                column: "SupplyUnitsId",
                principalTable: "SupplyUnit",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_SupplySupplyUnit_Supply_SuppliesId",
                table: "SupplySupplyUnit",
                column: "SuppliesId",
                principalTable: "Supply",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_SupplyUnit_Products_ProductId",
                table: "SupplyUnit",
                column: "ProductId",
                principalTable: "Products",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}