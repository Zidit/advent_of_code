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

pub fn main() !void {
    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var total: u64 = 0;

    var lines = std.mem.splitSequence(u8, input, "\r\n");
    while (lines.next()) |line| {
        const initial_secret = try std.fmt.parseInt(u32, line, 10);
        var secret = initial_secret;
        for (0..2000) |_|
            secret = calc_secret(secret);

        total += secret;
        //std.debug.print("{d}: {d}\n", .{ initial_secret, secret });
    }

    std.debug.print("{d}\n", .{total});
}
