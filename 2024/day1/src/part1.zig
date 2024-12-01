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
    var right = std.ArrayList(u32).init(std.heap.page_allocator);
    defer left.deinit();
    defer right.deinit();

    var lines = std.mem.splitSequence(u8, input, "\r\n");
    while (lines.next()) |line| {
        var parts = std.mem.tokenizeScalar(u8, line, ' ');
        const l = try std.fmt.parseUnsigned(u32, parts.next().?, 10);
        const r = try std.fmt.parseUnsigned(u32, parts.next().?, 10);
        try left.append(l);
        try right.append(r);

        //std.debug.print("'{d} - {d}'\n", .{ l, r });
    }

    //std.debug.print("{any}\n", .{left});
    //std.debug.print("{any}\n", .{right});

    const l_data = try left.toOwnedSlice();
    const r_data = try right.toOwnedSlice();

    std.mem.sort(u32, l_data, {}, std.sort.desc(u32));
    std.mem.sort(u32, r_data, {}, std.sort.desc(u32));

    var total: u64 = 0;
    for (l_data, r_data) |l, r| {
        total += @abs(@as(i64, l) - @as(i64, r));
    }

    std.debug.print("{any}", .{total});
}
