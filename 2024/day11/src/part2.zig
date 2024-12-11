const std = @import("std");

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn digits(v: u64) u64 {
    var c: usize = 1;
    var t: u64 = v;
    while (t >= 10) {
        t /= 10;
        c += 1;
    }

    return c;
}

const Key = struct { s: u64, b: u8 };
var cache: std.AutoHashMap(Key, u64) = undefined;

fn stones(v: u64, blink: u8) !u64 {
    if (blink == 0) {
        return 1;
    }

    const key = .{ .s = v, .b = blink };
    if (cache.contains(key)) {
        return cache.get(key).?;
    }

    var result: u64 = 0;
    if (v == 0) {
        result = try stones(1, blink - 1);
    } else {
        const d = digits(v);
        if (d % 2 == 0) {
            const a: u64 = v / std.math.pow(u64, 10, d / 2);
            const b: u64 = v % std.math.pow(u64, 10, d / 2);
            result = try stones(a, blink - 1) + try stones(b, blink - 1);
        } else {
            result = try stones(v * 2024, blink - 1);
        }
    }

    try cache.put(key, result);
    return result;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    cache = std.AutoHashMap(Key, u64).init(allocator);

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var total: u64 = 0;
    var values = std.mem.splitSequence(u8, input, " ");
    while (values.next()) |v| {
        total += try stones(try std.fmt.parseInt(u64, v, 10), 75);
    }

    std.debug.print("{d}\n", .{total});
}
