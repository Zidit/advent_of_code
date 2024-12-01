const std = @import("std");

fn read_input() ![]u8 {
    const file = try std.fs.cwd().openFile("src/input.txt", .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

pub fn main() !void {
    const input = try read_input();
    //try stdout.print("Input: {s}\n", .{input});

    var left = std.ArrayList(u32).init(std.heap.page_allocator);
    var right = std.AutoHashMap(u32, u32).init(std.heap.page_allocator);
    defer left.deinit();
    defer right.deinit();

    var lines = std.mem.splitSequence(u8, input, "\r\n");
    while (lines.next()) |line| {
        var parts = std.mem.tokenizeScalar(u8, line, ' ');
        const l = try std.fmt.parseUnsigned(u32, parts.next().?, 10);
        const r = try std.fmt.parseUnsigned(u32, parts.next().?, 10);

        try left.append(l);
        try right.put(r, (right.get(r) orelse 0) + 1);
    }

    const l_data = try left.toOwnedSlice();

    var total: u64 = 0;
    for (l_data) |l| {
        total += l * (right.get(l) orelse 0);
    }

    std.debug.print("{any}", .{total});
}
