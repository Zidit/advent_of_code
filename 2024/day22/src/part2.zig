const std = @import("std");

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn split_string(input: []const u8, delim: []const u8, allocator: std.mem.Allocator) ![][]const u8 {
    var arr = std.ArrayList([]const u8).init(allocator);
    defer arr.deinit();

    var parts = std.mem.splitSequence(u8, input, delim);
    while (parts.next()) |p| {
        try arr.append(p);
    }

    return arr.toOwnedSlice();
}

fn calc_secret(secret_in: u32) u32 {
    var secret: u64 = secret_in;

    secret ^= secret * 64;
    secret &= 0xFFFFFF;

    secret ^= secret / 32;
    secret &= 0xFFFFFF;

    secret ^= secret * 2048;
    secret &= 0xFFFFFF;

    return @truncate(secret);
}

fn get_sellpoints(initial_secret: u32, allocator: std.mem.Allocator) !std.AutoHashMap(u32, i32) {
    var secret = initial_secret;
    var prev_price: i32 = @intCast(initial_secret % 10);

    var key: u32 = 0;
    var sell_points = std.AutoHashMap(u32, i32).init(allocator);

    for (0..2000) |i| {
        secret = calc_secret(secret);
        const price: i32 = @intCast(secret % 10);
        const delta = price - prev_price;
        prev_price = price;

        key <<= 8;
        const tmp: u32 = @intCast(delta + 10);
        key |= tmp & 0xFF;
        if (i > 4 and !sell_points.contains(key))
            try sell_points.put(key, price);
    }

    return sell_points;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var total_prices = std.AutoHashMap(u32, i32).init(allocator);

    var lines = std.mem.splitSequence(u8, input, "\r\n");
    while (lines.next()) |line| {
        const initial_secret = try std.fmt.parseInt(u32, line, 10);
        var new_prices = try get_sellpoints(initial_secret, allocator);

        var iter = new_prices.iterator();
        while (iter.next()) |entry| {
            const k = entry.key_ptr.*;
            const v = entry.value_ptr.*;

            if (total_prices.contains(k)) {
                const new = v + total_prices.get(k).?;
                try total_prices.put(k, new);
            } else {
                try total_prices.put(k, v);
            }
        }

        new_prices.deinit();
    }

    var tot_iter = total_prices.iterator();
    var best: i32 = 0;

    while (tot_iter.next()) |entry| {
        //const k = entry.key_ptr.*;
        const v = entry.value_ptr.*;

        if (v > best) {
            best = v;

            //const a: i8 = @intCast((k >> 24) & 0xFF);
            //const b: i8 = @intCast((k >> 16) & 0xFF);
            //const c: i8 = @intCast((k >> 8) & 0xFF);
            //const d: i8 = @intCast((k >> 0) & 0xFF);
            //std.debug.print("{d},{d},{d},{d}: {d}\n", .{ a - 10, b - 10, c - 10, d - 10, v });
        }
    }

    std.debug.print("{d}\n", .{best});
}
