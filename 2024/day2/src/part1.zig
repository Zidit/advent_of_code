const std = @import("std");

fn read_input() ![]u8 {
    const file = try std.fs.cwd().openFile("src/input.txt", .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn is_safe(reports: []const i8) !bool {
    var dir: i8 = 0;
    var prev: i8 = 0;
    for (reports) |v| {
        if (prev == 0) {
            prev = v;
            continue;
        } else if (dir == 0) {
            dir = if (v < prev) -1 else 1;
        }

        const diff = (v - prev) * dir;
        if (diff < 1 or diff > 3) {
            return false;
        }
        prev = v;
    }

    return true;
}

pub fn main() !void {
    const input = try read_input();

    var safe_reports: u32 = 0;
    var lines = std.mem.splitSequence(u8, input, "\r\n");
    while (lines.next()) |line| {
        var reports = std.BoundedArray(i8, 10){};
        var values = std.mem.tokenizeScalar(u8, line, ' ');
        while (values.next()) |value| {
            try reports.append(try std.fmt.parseUnsigned(i8, value, 10));
        }

        //std.debug.print("{any} ", .{reports});
        if (try is_safe(reports.slice())) {
            safe_reports += 1;
            //std.debug.print("safe\n ", .{});
        } else {
            //std.debug.print("not safe\n ", .{});
        }
    }

    std.debug.print("{any}", .{safe_reports});
}
