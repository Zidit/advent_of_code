const std = @import("std");

const File = struct { id: i16, size: u8 };

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

    var data_exp = std.ArrayList(File).init(allocator);
    defer data_exp.deinit();

    var id: i16 = 0;
    var is_file: bool = true;

    for (input) |c| {
        const v = c - '0';
        const f: File = .{ .id = if (is_file) id else -1, .size = v };
        try data_exp.append(f);

        if (is_file) {
            id += 1;
        }
        is_file = !is_file;
    }

    //std.debug.print("{any}\n", .{data_exp.items});

    //for (data_exp.items) |f| {
    //    var o: u8 = '0';
    //    if (f.id < 0) {
    //        o = '.';
    //    } else {
    //        o += @intCast(f.id);
    //    }
    //
    //    var i: u16 = 0;
    //    while (i < f.size) : (i += 1)
    //        std.debug.print("{c}", .{o});
    //}
    //std.debug.print("\n", .{});

    var move_pos = data_exp.items.len - 1;

    while (move_pos > 0) : (move_pos -= 1) {
        const f = data_exp.items[move_pos];
        if (f.id < 0) {
            continue;
        }
        //std.debug.print("{any}", .{f});

        for (data_exp.items, 0..) |t, i| {
            if (t.id >= 0)
                continue;
            if (t.size < f.size)
                continue;
            if (i >= move_pos)
                break;

            data_exp.items[i].size -= f.size;
            data_exp.items[move_pos].id = -1;
            try data_exp.insert(i, f);
            break;
        }
    }

    //for (data_exp.items) |f| {
    //    var o: u8 = '0';
    //    if (f.id < 0) {
    //        o = '.';
    //    } else {
    //        o += @intCast(f.id);
    //    }
    //
    //    var i: u16 = 0;
    //    while (i < f.size) : (i += 1)
    //        std.debug.print("{c}", .{o});
    //}
    //std.debug.print("\n", .{});

    var pos: u64 = 0;
    var total: u64 = 0;
    for (data_exp.items) |f| {
        if (f.id < 0) {
            pos += f.size;
            continue;
        }

        var i: u16 = 0;
        while (i < f.size) : (i += 1) {
            const tmp: u64 = @intCast(f.id);
            total += pos * tmp;
            pos += 1;
        }
    }

    std.debug.print("{d}", .{total});
}
