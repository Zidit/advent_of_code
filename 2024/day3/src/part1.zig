const std = @import("std");

fn read_input() ![]u8 {
    const file = try std.fs.cwd().openFile("src/input.txt", .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn parse_inner(inner: []const u8) !struct { a: u32, b: u32 } {
    const sep = std.mem.indexOf(u8, inner, ",") orelse return std.fmt.ParseIntError.InvalidCharacter;
    const a = try std.fmt.parseUnsigned(u32, inner[0..sep], 10);
    const b = try std.fmt.parseUnsigned(u32, inner[sep + 1 ..], 10);

    return .{ .a = a, .b = b };
}

pub fn main() !void {
    const input = try read_input();
    //const input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";

    var total: u32 = 0;
    var pos: usize = 0;
    while (std.mem.indexOfPos(u8, input, pos, "mul(")) |p| {
        const end = std.mem.indexOfPos(u8, input, p, ")") orelse break;
        const inner: []const u8 = input[p + 4 .. end];

        //std.debug.print("found mem @ {d} -> {s}\n", .{ p, inner });

        if (parse_inner(inner)) |i| {
            //std.debug.print("values {d},{d}\n", .{ i.a, i.b });
            total += i.a * i.b;
            pos = end + 1;
        } else |_| {
            //std.debug.print("failed to parse inner\n", .{});
            pos = p + 4;
        }
    }

    std.debug.print("{d}\n", .{total});
}
