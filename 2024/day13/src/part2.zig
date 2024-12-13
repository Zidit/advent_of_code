const std = @import("std");

const Vec2 = struct {
    x: i64,
    y: i64,

    pub fn init(x: i64, y: i64) Vec2 {
        return .{ .x = x, .y = y };
    }

    pub fn init_u(x: u32, y: u32) Vec2 {
        return .{ .x = @intCast(x), .y = @intCast(y) };
    }

    pub fn add(self: Vec2, other: Vec2) Vec2 {
        return .{ .x = self.x + other.x, .y = self.y + other.y };
    }

    pub fn equal(self: Vec2, other: Vec2) bool {
        return self.x == other.x and self.y == other.y;
    }
};

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

fn split_line(line_in: []const u8) !Vec2 {
    const line = std.mem.trim(u8, line_in, " \n\r");
    //std.debug.print("-{s}-\n", .{line});

    var a = std.mem.splitSequence(u8, line, ":");
    _ = a.next();

    var b = std.mem.splitAny(u8, a.next().?, "+=,");
    _ = b.next();
    const x = try std.fmt.parseInt(i64, b.next().?, 10);
    _ = b.next();
    const y = try std.fmt.parseInt(i64, b.next().?, 10);

    return .{ .x = x, .y = y };
}

fn get_price(a: Vec2, b: Vec2, t: Vec2) !Vec2 {
    if (@rem(t.y * b.x - b.y * t.x, a.y * b.x - b.y * a.x) != 0)
        return error.OutOfRange;
    const ao = @divExact(t.y * b.x - b.y * t.x, a.y * b.x - b.y * a.x);

    if (@rem(t.x - ao * a.x, b.x) != 0)
        return error.OutOfRange;
    const bo = @divExact(t.x - ao * a.x, b.x);

    return Vec2.init(ao, bo);
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    //const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var total: i64 = 0;
    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.peek()) |_| {
        const a = try split_line(lines.next().?);
        const b = try split_line(lines.next().?);
        var t = try split_line(lines.next().?);
        _ = lines.next();

        t.x += 10000000000000;
        t.y += 10000000000000;

        //std.debug.print("{any}, {any}, {any} = ", .{ a, b, t });
        const price = get_price(a, b, t) catch Vec2.init(0, 0);
        //std.debug.print("{any}\n", .{price});

        total += price.x * 3 + price.y;
    }

    std.debug.print("{d}\n", .{total});
}
