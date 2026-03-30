using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace StorageServer.Migrations
{
    /// <inheritdoc />
    public partial class add_AppUserIsGenerated : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "IsGenerated",
                table: "Users",
                type: "bit",
                nullable: false,
                defaultValue: false);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "IsGenerated",
                table: "Users");
        }
    }
}
