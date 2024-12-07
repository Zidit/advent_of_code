const std = @import("std");

const Vec2 = struct { x: i32, y: i32 };

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn test_equ_mul(target: u64, start: u64, values: []u64) bool {
    const sum = start * values[0];
    if (values.len == 1)
        return target == sum;

    if (sum > target)
        return false;

    if (test_equ_sum(target, sum, values[1..]))
        return true;

    if (test_equ_mul(target, sum, values[1..]))
        return true;

    return false;
}

fn test_equ_sum(target: u64, start: u64, values: []u64) bool {
    const sum = start + values[0];
    if (values.len == 1)
        return target == sum;

    if (sum > target)
        return false;

    if (test_equ_sum(target, sum, values[1..]))
        return true;

    if (test_equ_mul(target, sum, values[1..]))
        return true;

    return false;
}

fn test_equ(target: u64, values: []u64) bool {
    std.debug.print("Test: {d} = {any} - ", .{ target, values });

    const is_valid = test_equ_sum(target, 0, values);

    std.debug.print("{any}\n", .{is_valid});

    return is_valid;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var total: u64 = 0;
    var lines = std.mem.tokenizeScalar(u8, input, '\n');
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        const sep = std.mem.indexOfScalar(u8, line_trimmed, ':').?;

        const target = try std.fmt.parseUnsigned(u64, line_trimmed[0..sep], 10);

        var values = std.ArrayList(u64).init(allocator);
        defer values.deinit();

        var val_iter = std.mem.tokenizeScalar(u8, line_trimmed[sep + 1 ..], ' ');
        while (val_iter.next()) |val_str| {
            try values.append(try std.fmt.parseUnsigned(u64, val_str, 10));
        }

        if (test_equ(target, values.items))
            total += target;
    }

    std.debug.print("{d}", .{total});
}
