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

fn get_combo(a: i64, b: i64, c: i64, op: i64) i64 {
    if (op == 4) {
        return a;
    } else if (op == 5) {
        return b;
    } else if (op == 6) {
        return c;
    }
    return op;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var lines = std.mem.splitSequence(u8, input, "\r\n");

    //std.debug.print("reg_a: {any}\n", .{(try split_string(lines.next().?, ": ", allocator))[1]});

    var reg_a: i64 = try std.fmt.parseInt(i64, (try split_string(lines.next().?, ": ", allocator))[1], 10);
    var reg_b: i64 = try std.fmt.parseInt(i64, (try split_string(lines.next().?, ": ", allocator))[1], 10);
    var reg_c: i64 = try std.fmt.parseInt(i64, (try split_string(lines.next().?, ": ", allocator))[1], 10);
    _ = lines.next();

    var prog = std.ArrayList(i64).init(allocator);
    var iter = std.mem.splitScalar(u8, (try split_string(lines.next().?, ": ", allocator))[1], ',');
    while (iter.next()) |p| {
        try prog.append(try std.fmt.parseInt(i64, p, 10));
    }

    std.debug.print("reg_a: {d}\n", .{reg_a});
    std.debug.print("reg_b: {d}\n", .{reg_b});
    std.debug.print("reg_c: {d}\n", .{reg_c});
    std.debug.print("prog: {any}\n", .{prog.items});

    var pc: usize = 0;
    var out = std.ArrayList(i64).init(allocator);

    var timeout: u32 = 200000;
    while (timeout > 0) {
        timeout -= 1;
        if (pc + 1 > prog.items.len)
            break;
        const opcode: i64 = prog.items[pc];
        const operand: i64 = prog.items[pc + 1];
        const combo: i64 = get_combo(reg_a, reg_b, reg_c, operand);

        //std.debug.print("pc: {d}, opcode: {d}, operand: {d}, combo: {d}\n", .{ pc, opcode, operand, combo });

        pc += 2;

        switch (opcode) {
            0 => { //adv
                const combo3: u3 = @intCast(combo);
                reg_a = reg_a >> combo3;
            },
            1 => { //blx
                reg_b = reg_b ^ operand;
            },
            2 => { //bst
                reg_b = combo & 0x7;
            },
            3 => { //jnz
                if (reg_a != 0)
                    pc = @intCast(operand);
            },
            4 => { //bxc
                reg_b = reg_b ^ reg_c;
            },
            5 => { //out
                //std.debug.print("{d}\n", .{combo & 0x7});
                try out.append(combo & 0x7);
            },
            6 => { //bdv
                const combo3: u3 = @intCast(combo);
                reg_b = reg_a >> combo3;
            },
            7 => { //cdv
                const combo3: u3 = @intCast(combo);
                reg_c = reg_a >> combo3;
            },

            else => {
                std.debug.print("unknown opcode: {d}\n", .{opcode});
                break;
            },
        }

        //std.debug.print("reg_a: {d}, reg_b: {d}, reg_c: {d}\n\n", .{ reg_a, reg_b, reg_c });
    }

    for (out.items) |item| {
        std.debug.print("{d},", .{item});
    }
}
