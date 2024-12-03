const std = @import("std");

var do: bool = true;

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

fn find_next(input: []const u8, pos: usize) ?usize {
    const mul_pos = std.mem.indexOfPos(u8, input, pos, "mul(");
    const do_pos = std.mem.indexOfPos(u8, input, pos, "do()");
    const dont_pos = std.mem.indexOfPos(u8, input, pos, "don't()");

    if (mul_pos == null) return null;

    if (do_pos != null) {
        if (do_pos.? < mul_pos.? and do_pos.? < (dont_pos orelse std.math.maxInt(usize))) {
            do = true;
            return find_next(input, pos + 4);
        }
    }

    if (dont_pos != null) {
        if (dont_pos.? < mul_pos.?) {
            do = false;
            return find_next(input, pos + 7);
        }
    }

    return mul_pos;
}

pub fn main() !void {
    const input = try read_input();
    //const input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";

    var total: u32 = 0;
    var pos: usize = 0;
    while (find_next(input, pos)) |p| {
        const end = std.mem.indexOfPos(u8, input, p, ")") orelse break;
        const inner: []const u8 = input[p + 4 .. end];

        if (parse_inner(inner)) |i| {
            if (do)
                total += i.a * i.b;
            pos = end + 1;
        } else |_| {
            pos = p + 4;
        }
    }

    std.debug.print("{d}\n", .{total});
}
