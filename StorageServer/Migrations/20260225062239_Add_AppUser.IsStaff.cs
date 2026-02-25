using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace StorageServer.Migrations
{
    /// <inheritdoc />
    public partial class Add_AppUserIsStaff : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "IsStaff",
                table: "AppUser",
                type: "bit",
                nullable: false,
                defaultValue: false);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "IsStaff",
                table: "AppUser");
        }
    }
}
