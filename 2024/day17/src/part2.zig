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

fn run_prog(a: i64, b: i64, c: i64, prog: []i64) ?i64 {
    var reg_a: i64 = a;
    var reg_b: i64 = b;
    var reg_c: i64 = c;

    var pc: usize = 0;

    var timeout: u32 = 200000;
    while (timeout > 0) {
        timeout -= 1;
        if (pc + 1 > prog.len)
            break;
        const opcode: i64 = prog[pc];
        const operand: i64 = prog[pc + 1];
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
                std.debug.print("{d},", .{combo & 0x7});
                //try out.append(combo & 0x7);
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

    std.debug.print("\n", .{});

    return null;
}

fn run_prog_for_first_output(a: i64, b: i64, c: i64, prog: []i64) ?i64 {
    var reg_a: i64 = a;
    var reg_b: i64 = b;
    var reg_c: i64 = c;

    var pc: usize = 0;

    var timeout: u32 = 200000;
    while (timeout > 0) {
        timeout -= 1;
        if (pc + 1 > prog.len)
            break;
        const opcode: i64 = prog[pc];
        const operand: i64 = prog[pc + 1];
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
                //try out.append(combo & 0x7);
                return combo & 0x7;
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

    return null;
}

fn find_common(a: []u12, b: []u12, bytes: u4, allocator: std.mem.Allocator) !std.ArrayList(u12) {
    var ret = std.ArrayList(u12).init(allocator);

    for (a) |at| {
        for (b) |bt| {
            if (match(at, bt, bytes)) {
                try ret.append(bt);
                break;
            }
        }
    }

    return ret;
}

fn match(a: u12, b: u12, bytes: u4) bool {
    return (a >> bytes) == (b & (@as(u12, 0xfff) >> bytes));
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var lines = std.mem.splitSequence(u8, input, "\r\n");

    //std.debug.print("reg_a: {any}\n", .{(try split_string(lines.next().?, ": ", allocator))[1]});

    const reg_a: i64 = try std.fmt.parseInt(i64, (try split_string(lines.next().?, ": ", allocator))[1], 10);
    const reg_b: i64 = try std.fmt.parseInt(i64, (try split_string(lines.next().?, ": ", allocator))[1], 10);
    const reg_c: i64 = try std.fmt.parseInt(i64, (try split_string(lines.next().?, ": ", allocator))[1], 10);
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

    // The output depends only on first 10 bits of register A. Calculate all combinations into a map.
    //var inout = std.AutoHashMap(i64, i64).init(allocator);
    var inout: [8]std.ArrayList(u64) = .{std.ArrayList(u64).init(allocator)} ** 8;

    for (0..1024) |a| {
        const out = run_prog_for_first_output(@intCast(a), reg_b, reg_c, prog.items);
        if (out) |o| {
            const i: usize = @intCast(o);
            const v: u64 = @intCast(a);
            try inout[i].append(v);
            //try inout.put(@intCast(a), o);
        } else {
            std.debug.print("no output for {d}\n", .{a});
        }
    }

    //std.debug.print("inout: {any}\n", .{inout});

    const prog_rev = try prog.clone();
    std.mem.reverse(i64, prog_rev.items);

    var valid_inputs = std.ArrayList(u64).init(allocator);
    const first: usize = @intCast(prog_rev.items[0]);
    try valid_inputs.appendSlice(inout[first].items);

    for (prog_rev.items[1..]) |p| {
        //std.debug.print("inputs:  {any}\n", .{valid_inputs.items});
        const t: usize = @intCast(p);
        const new_candidates = inout[t].items;
        var new_valid_inputs = std.ArrayList(u64).init(allocator);

        for (valid_inputs.items) |v| {
            for (new_candidates) |nc| {
                if ((v & 0x7f) == (nc >> 3)) {
                    const val = v << 3;
                    const new_val = val | nc;
                    //std.debug.print("v: {d}, nc: {d}, new {d}\n", .{ v, nc, new_val });
                    try new_valid_inputs.append(new_val);
                }
            }
        }

        valid_inputs.deinit();
        valid_inputs = new_valid_inputs;
    }

    std.mem.sort(u64, valid_inputs.items, void{}, std.sort.asc(u64));

    //for (valid_inputs.items) |vi| {
    //    std.debug.print("\n{any}\n", .{vi});
    //    const a: i64 = @intCast(vi);
    //    _ = run_prog(a, reg_b, reg_c, prog.items);
    //}

    std.debug.print("{d}\n", .{valid_inputs.items[0]});
}
