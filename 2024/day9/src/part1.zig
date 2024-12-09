const std = @import("std");

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var data_exp = std.ArrayList(?u16).init(allocator);
    defer data_exp.deinit();

    var id: u16 = 0;
    var is_file: bool = true;

    for (input) |c| {
        const v = c - '0';
        var i: u8 = 0;
        if (is_file) {
            while (i < v) : (i += 1) {
                try data_exp.append(id);
            }
            id += 1;
        } else {
            while (i < v) : (i += 1) {
                try data_exp.append(null);
            }
        }

        is_file = !is_file;
    }

    //for (data_exp.items) |c| {
    //    var o: u8 = '.';
    //    if (c != null) {
    //        o = '0';
    //        o += @intCast(c.?);
    //    }
    //    std.debug.print("{c}", .{o});
    //}
    //std.debug.print("\n", .{});

    var data = try data_exp.toOwnedSlice();
    var s_pos = std.mem.indexOfScalar(?u16, data, null);
    var e_pos = std.mem.lastIndexOfNone(?u16, data, &[_]?u16{null});

    while (true) {
        //std.debug.print("{any}, {any}\n", .{ s_pos, e_pos });
        if (s_pos == null or e_pos == null or s_pos.? > e_pos.?)
            break;

        data[s_pos.?] = data[e_pos.?];
        data[e_pos.?] = null;

        s_pos = std.mem.indexOfScalar(?u16, data, null);
        e_pos = std.mem.lastIndexOfNone(?u16, data, &[_]?u16{null});
    }

    //for (data) |c| {
    //    var o: u8 = '.';
    //    if (c != null) {
    //        o = '0';
    //        o += @intCast(c.?);
    //    }
    //    std.debug.print("{c}", .{o});
    //}
    //std.debug.print("\n", .{});

    var total: u64 = 0;
    for (data, 0..) |c, i| {
        if (c) |v| {
            total += v * i;
        }
    }
    std.debug.print("{d}", .{total});
}
